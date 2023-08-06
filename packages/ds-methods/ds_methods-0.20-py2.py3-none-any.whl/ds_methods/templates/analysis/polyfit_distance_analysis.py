from pandas import DataFrame
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.analysis import *
from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling
from ds_methods.templates.init_data import load_raw_data


def polyfit(series, degree):
    X = [i % period for i in range(len(series))]

    y = series.values
    coef = np.polyfit(X[period:3 * period], y[period:3 * period], degree)
    curve = []
    for i in range(len(X)):
        value = coef[-1]
        for d in range(degree):
            value += X[i] ** (degree - d) * coef[d]
        curve.append(value)

    return curve


data = load_raw_data(is_only_full=True)

infection_date = datetime(2020, 11, 4, 12, 00, 00)
poly_degree = 3
n_resample_minutes = 4
period = 24 * 60 // n_resample_minutes
distance_window_hours = 12
full_distance_length = distance_window_hours * 60 // n_resample_minutes
columns = ['area', 'size', 'temperature', 'speed', 'rotation', 'temperature_speed']

data = data[data['condition'] == 'healthy']
print(data)

degrees_range = range(2, 18)
columns_distances = {}

for name, group in data.groupby('target'):
    if name in ['25', '26', '27', '31', '32']:
        print(name)
        group = group.reset_index(drop=True)
        day_groups = Group({'time': 24.}).make(group)['data']

        dates = []
        for day, day_group in day_groups:
            if not day_group.empty:
                dates.append([day_group.index[0], day.date()])

        for column in columns:
            if column not in columns_distances:
                columns_distances[column] = {}

            clear = Pipeline([
                Group({'time': 2}),
                FilterOutliers({'include': [column], 'threshold': .5, 'how': 'any'}),
                Resampling({'rule': f'{n_resample_minutes}Min'}),
            ], verbose=0).run(group)['data']
            series = clear[column]
            sd = SeasonalDecomposition({'period': period, 'is_extrapolate': True}).make(clear)['data']

            columns_distances[column][name] = {'distances': [], 'curves': [], 'series': series, 'sd': sd[column], 'dates': dates}

            for degree in degrees_range:
                curve = polyfit(series, degree=degree)
                curve = (curve + sd[column] - np.array(curve).mean()).tolist()

                distance = np.linalg.norm(series - curve)
                columns_distances[column][name]['distances'].append(1/distance)
                if degree % 4 == 0:
                    columns_distances[column][name]['curves'].append({'degree': degree, 'data': curve})

for column in columns:
    mice_count = len(list(columns_distances[column].values()))
    _, axes = plt.subplots(1 + mice_count, figsize=(16, 6 * mice_count))

    for index, mouse_name in enumerate(columns_distances[column]):
        distances = columns_distances[column][mouse_name]
        normalized_distances = Normalisation({'type': 'min_max'})\
            .make(DataFrame({'distances': distances['distances']}))['data']['distances']\
            .to_list()
        axes[0].plot(normalized_distances, linewidth=0.8, alpha=0.8)

        axes[1 + index].plot(distances['series'], linewidth=0.8, alpha=0.8)
        axes[1 + index].plot(distances['sd'], linewidth=2, alpha=0.8)
        for curve in distances['curves']:
            axes[1 + index].plot(curve['data'], linewidth=3, alpha=0.8)

    axes[0].set_ylabel('inverse normalized distance')
    axes[0].set_xlabel('polynomial degree')
    axes[0].set_title(
        f'Normalized Distance plots for each mouse for different polynomial fit degree\n'
        f'Feature - {column}',
    )
    axes[0].set_xticks(list(range(len(list(degrees_range)))))
    axes[0].set_xticklabels(list(degrees_range))
    axes[0].legend(list(map(lambda x: f'Mouse - {x}', columns_distances[column].keys())), loc=1)

    for index, mouse_name in enumerate(columns_distances[column]):
        distances = columns_distances[column][mouse_name]

        axes[1 + index].set_ylabel(f'Mouse {mouse_name}, Feature - {column}')
        axes[1 + index].set_xticks(list(zip(*distances['dates']))[0])
        axes[1 + index].set_xticklabels(list(zip(*distances['dates']))[1], rotation=30)
        axes[1 + index].legend(
            ['raw', 'trend'] + [f'poly degree {curve["degree"]}' for curve in distances['curves']],
            loc=1,
        )

    plt.savefig(f'plots/{column}.png')
