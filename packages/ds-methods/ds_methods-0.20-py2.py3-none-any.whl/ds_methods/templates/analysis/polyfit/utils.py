import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

from ds_methods.methods.groups import *


def quadratic_spline_roots(spl):
    roots = []
    knots = spl.get_knots()
    for a, b in zip(knots[:-1], knots[1:]):
        u, v, w = spl(a), spl((a+b)/2), spl(b)
        t = np.roots([u+w-2*v, w-u, 2*v])
        t = t[np.isreal(t) & (np.abs(t) <= 1)]
        roots.extend(t*(b-a)/2 + (b+a)/2)
    return np.array(roots)


def polyfit(series, degree=4, is_numpy=False, sparcing=1):
    X = list(range(len(series)))
    y = series.values.tolist()

    if is_numpy:
        poly = np.poly1d(np.polyfit(X[::sparcing], y[::sparcing], degree))
    else:
        y_mean = [2 * sum(y[:sparcing // 2]) // sparcing]
        for i in range(sparcing, len(y) - 1, sparcing):
            y_window = y[i - sparcing // 2: i + sparcing // 2 + 1]
            y_mean.append(sum(y_window) / len(y_window))
        y_mean.append(2 * sum(y[-(sparcing // 2):]) // sparcing)

        x = X[::sparcing] + [X[-1]]

        poly = InterpolatedUnivariateSpline(x, y_mean, k=3)
        # poly = interp1d(x, y_mean, kind='cubic')

    return {
        'data': poly(X),
        'poly': poly,
    }


def get_days_dates(group):
    day_groups = Group({'time': 24}).make(group)['data']

    dates = []
    for day, day_group in day_groups:
        if not day_group.empty:
            dates.append([day_group.index[0], day.date()])

    return dates


def get_polynomial_info(series, sparcing):
    polynomial = polyfit(series, sparcing=sparcing)
    data = polynomial['data']
    poly = polynomial['poly']

    local_extremas_x = quadratic_spline_roots(poly.derivative())

    x_maxes = [int(x) for x in local_extremas_x if poly.derivatives(x)[2] < 0]
    y_maxes = poly(x_maxes)

    x_mins = [int(x) for x in local_extremas_x if poly.derivatives(x)[2] > 0]
    y_mins = poly(x_mins)

    return {
        'data': data,
        'mins': {'x': x_mins, 'y': y_mins},
        'maxes': {'x': x_maxes, 'y': y_maxes},
    }


def get_polynomial_statistics(polynomial_data, polynomial_mins, polynomial_maxes, search_window):
    all_extremas = sorted(
        list(zip(polynomial_mins['x'], polynomial_mins['y'])) + list(zip(polynomial_maxes['x'], polynomial_maxes['y'])),
        key=lambda x: x[0],
    )

    extremas_by_window = split_by_search_window(
        all_extremas,
        window=search_window,
        total_windows=len(polynomial_data) // search_window,
        key=0,
    )
    maxes_by_window = split_by_search_window(
        polynomial_maxes['x'],
        window=search_window,
        total_windows=len(polynomial_data) // search_window,
    )
    mins_by_window = split_by_search_window(
        polynomial_mins['x'],
        window=search_window,
        total_windows=len(polynomial_data) // search_window,
    )
    maxes_count = [len(window) for window in maxes_by_window]
    mins_count = [len(window) for window in mins_by_window]

    distances_between_maxes = diff(polynomial_maxes['x'])
    distances_between_mins = diff(polynomial_mins['x'])
    distances_between_maxes_and_mins = diff([0] + [x[0] for x in all_extremas])
    mean_extremas_distance_by_day = [
        np.array(diff([x[0] for x in window])).mean() if len(window) > 1 else 0
        for window in extremas_by_window
    ]

    heights_between_maxes = diff(polynomial_maxes['y'])
    heights_between_mins = diff(polynomial_mins['y'])
    heights_between_maxes_and_mins = diff([polynomial_data[0]] + [x[1] for x in all_extremas])
    mean_extremas_height_by_day = [
        np.array(diff([x[1] for x in window])).mean() if len(window) > 1 else 0
        for window in extremas_by_window
    ]

    return {
        'maxes_count': maxes_count,
        'mins_count': mins_count,
        'distances_between_maxes': distances_between_maxes,
        'distances_between_mins': distances_between_mins,
        'distances_between_maxes_and_mins': distances_between_maxes_and_mins,
        'mean_extremas_distance_by_day': mean_extremas_distance_by_day,
        'heights_between_maxes': heights_between_maxes,
        'heights_between_mins': heights_between_mins,
        'heights_between_maxes_and_mins': heights_between_maxes_and_mins,
        'mean_extremas_height_by_day': mean_extremas_height_by_day,
    }


def split_by_search_window(series, window, total_windows, key=None):
    by_window = [[] for window in range(total_windows)]
    for x in series:
        if key is not None:
            by_window[int(x[key] // window)].append(x)
        else:
            by_window[int(x // window)].append(x)

    return by_window


def diff(series, n=1):
    diffs = []
    for i in range(n, len(series)):
        diffs.append(series[i] - series[i - n])

    return diffs
