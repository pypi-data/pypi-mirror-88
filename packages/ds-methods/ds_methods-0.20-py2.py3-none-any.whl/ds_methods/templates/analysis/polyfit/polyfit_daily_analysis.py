import pandas as pd
from matplotlib import pyplot as plt

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.templates.init_data import load_raw_data
from ds_methods.templates.analysis.polyfit.consts import *
from ds_methods.templates.analysis.polyfit.utils import *


data = load_raw_data(is_only_full=True, n_resample_minutes=RESAMPLE_MINUTES)
data = Pipeline([
    Group({'keys': ['target']}),
    FilterOutliers({'threshold': 3, 'how': 'any'}),
    Group({'keys': ['target']}),
    MovingAverage({'time': '2h'}),
]).run(data)['data']


def polyfit_dayli_analysis(is_plot=True):
    results = {}
    for name, group in data.groupby('target'):
        if name in MICE_NAMES:
            results[name] = {}
            print(name)
            group = group.reset_index(drop=True)
            sd = SeasonalDecomposition({'period': POINTS_PER_DAY, 'is_extrapolate': True}).make(group)['data']
            dates = get_days_dates(group)

            for column in COLUMNS:
                results[name][column] = {}
                print(column)
                series = group[column]
                series_sd = sd[column]

                polynomial_info = get_polynomial_info(series, INTERPOLATION_SPARCING)
                polynomial_data = polynomial_info['data']
                polynomial_maxes = polynomial_info['maxes']
                polynomial_mins = polynomial_info['mins']

                polynomial_statistics = get_polynomial_statistics(
                    polynomial_data,
                    polynomial_mins,
                    polynomial_maxes,
                    search_window=POINTS_PER_DAY,
                )
                polynomial_minus_trend = np.array(polynomial_data) - series_sd

                if is_plot:
                    _, axes = plt.subplots(9, figsize=(16, 45))

                    axes[0].bar(
                        [i for i in range(len(group)) if group['date'][i] >= INFECTION_DATE],
                        100000,
                        color='gray', width=1, alpha=0.15,
                    )
                    axes[0].plot(group[column], linewidth=2, alpha=0.8)
                    axes[0].plot(series_sd, linewidth=4, alpha=0.6)
                    axes[0].plot(polynomial_data, linewidth=5, alpha=0.6)
                    axes[0].scatter(polynomial_maxes['x'], polynomial_maxes['y'], color='darkred', s=200, alpha=1)
                    axes[0].scatter(polynomial_mins['x'], polynomial_mins['y'], color='darkblue', s=200, alpha=1)

                    axes[1].plot(polynomial_minus_trend, linewidth=4, alpha=0.6)
                    axes[1].scatter(polynomial_maxes['x'], np.array(polynomial_maxes['y']) - series_sd[polynomial_maxes['x']], color='darkred', s=200, alpha=1)
                    axes[1].scatter(polynomial_mins['x'], np.array(polynomial_mins['y']) - series_sd[polynomial_mins['x']], color='darkblue', s=200, alpha=1)

                    axes[2].bar(
                        range(len(polynomial_statistics['maxes_count'])),
                        polynomial_statistics['maxes_count'],
                        width=0.9, linewidth=7, alpha=0.5, align='edge',
                    )
                    axes[2].bar(
                        range(len(polynomial_statistics['mins_count'])),
                        polynomial_statistics['mins_count'],
                        width=0.7, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[3].bar(
                        range(len(polynomial_statistics['mean_extremas_distance_by_day'])),
                        polynomial_statistics['mean_extremas_distance_by_day'],
                        width=0.8, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[4].bar(
                        range(len(polynomial_statistics['mean_extremas_height_by_day'])),
                        polynomial_statistics['mean_extremas_height_by_day'],
                        width=0.8, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[5].bar(
                        range(len(polynomial_statistics['distances_between_maxes_and_mins'][::2])),
                        polynomial_statistics['distances_between_maxes_and_mins'][::2],
                        width=0.9, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[6].bar(
                        range(len(polynomial_statistics['heights_between_maxes_and_mins'][::2])),
                        polynomial_statistics['heights_between_maxes_and_mins'][::2],
                        width=0.9, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[7].bar(
                        range(len(polynomial_statistics['distances_between_maxes'])),
                        polynomial_statistics['distances_between_maxes'],
                        width=0.5, linewidth=7, alpha=0.5, align='edge',
                    )
                    axes[7].bar(
                        range(len(polynomial_statistics['distances_between_mins'])),
                        polynomial_statistics['distances_between_mins'],
                        width=0.8, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[8].bar(
                        range(len(polynomial_statistics['heights_between_maxes'])),
                        polynomial_statistics['heights_between_maxes'],
                        width=0.6, linewidth=7, alpha=0.5, align='edge',
                    )
                    axes[8].bar(
                        range(len(polynomial_statistics['heights_between_mins'])),
                        polynomial_statistics['heights_between_mins'],
                        width=0.8, linewidth=4, alpha=0.5, align='edge',
                    )

                    axes[0].set_title(
                        f'Polynomial statistics\n'
                        f'Mouse - {name}, Feature - {column},\n'
                    )
                    axes[0].legend([
                        'raw',
                        'trend',
                        'polynomials',
                        'local maximas',
                        'local minimas',
                    ], loc=1)
                    axes[0].set_xticks(list(zip(*dates))[0])
                    axes[0].set_xticklabels(list(zip(*dates))[1], rotation=30)
                    axes[0].set_ylim([
                        0.95*min([min(polynomial_data), group[column].min()]),
                        1.02*max([max(polynomial_data), group[column].max()]),
                    ])

                    axes[1].legend(['polynomial without trend'], loc=1)
                    axes[1].set_xticks(list(zip(*dates))[0])
                    axes[1].set_xticklabels(list(zip(*dates))[1], rotation=30)

                    axes[2].legend(['maxes_count', 'mins_count'], loc=1)
                    axes[2].set_xticks(list(range(len(dates))))
                    axes[2].set_xticklabels(list(zip(*dates))[1], rotation=30)

                    axes[3].legend(['mean_extremas_distance_by_day'], loc=1)
                    axes[3].set_xticks(list(range(len(dates))))
                    axes[3].set_xticklabels(list(zip(*dates))[1], rotation=30)

                    axes[4].legend(['mean_extremas_heights_by_day'], loc=1)
                    axes[4].set_xticks(list(range(len(dates))))
                    axes[4].set_xticklabels(list(zip(*dates))[1], rotation=30)

                    axes[5].legend(['distances_between_maxes_and_mins'], loc=1)

                    axes[6].legend(['heights_between_maxes_and_mins'], loc=1)

                    axes[7].legend(['distances_between_maxes', 'distances_between_mins'], loc=1)

                    axes[8].legend(['heights_between_maxes', 'heights_between_mins'], loc=1)

                    plt.savefig(f'plots/{name}_{column}.png')
                    plt.close('all')

                results[name][column] = {
                    'series': series,
                    'dates': dates,
                    'all_dates': group['date'],
                    'sd': series_sd,
                    'polynomial_info': polynomial_info,
                    'polynomial_minus_trend': polynomial_minus_trend,
                }

    return results


if __name__ == '__main__':
    polyfit_dayli_analysis()
