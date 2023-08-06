import pandas as pd
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
data = Pipeline([
    Group({'keys': ['target']}),
    FilterOutliers({'threshold': 3, 'how': 'any'}),
    Group({'keys': ['target']}),
    MovingAverage({'window': 15 * 3}),
]).run(data)['data']

infection_date = datetime(2020, 11, 4, 12, 00, 00)
poly_degree = 6
n_resample_minutes = 4
period = 24 * 60 // n_resample_minutes
distance_window_hours = 24
full_distance_length = distance_window_hours * 60 // n_resample_minutes
columns = ['area', 'size', 'temperature', 'speed']


for name, group in data.groupby('target'):
    if name in ['25', '26', '27', '31', '32']:
        print(name)
        group = group.reset_index(drop=True)

        day_groups = Group({'time': 24}).make(group)['data']

        dates = []
        for day, day_group in day_groups:
            if not day_group.empty:
                dates.append([day_group.index[0], day.date()])

        mice_distances = {}
        for column in columns:
            print(column)
            clear = Pipeline([
                Group({'time': 1}),
                # FilterOutliers({'include': [column], 'threshold': 1.5, 'how': 'any'}),
                Resampling({'rule': f'{n_resample_minutes}Min'}),
            ], verbose=0).run(group)['data']
            sd = SeasonalDecomposition({'period': period, 'is_extrapolate': True}).make(clear)['data']
            series = clear[column]
            sd['series'] = series
            sd['curve'] = polyfit(series, degree=poly_degree)
            sd['curve'] = (sd['curve'] + sd[column] - sd['curve'].mean()).tolist()
            sd = sd.dropna()

            distances = []
            window_groups = Group({'time': distance_window_hours}).make(sd)['data']
            for window_name, window_group in window_groups:
                distance = (np.linalg.norm(window_group['series'] - window_group['curve'])) * full_distance_length / len(window_group)
                distances += [distance] * full_distance_length

            sparced_distances = [0] + distances[::full_distance_length][1:]
            mice_distances[column] = sparced_distances.copy()
            differnces = [0]
            for i in range(1, len(sparced_distances) - 1):
                curr_difference = sparced_distances[i] / sparced_distances[i - 1]
                next_difference = sparced_distances[i + 1] / sparced_distances[i]

                differnces.append(next_difference / curr_difference)

            _, axes = plt.subplots(2, figsize=(16, 12))

            axes[0].bar(
                [i for i in range(len(group)) if group['date'][i] >= infection_date],
                1000000,
                color='gray', width=1, alpha=0.15,
            )
            axes[0].plot(series, linewidth=0.8, alpha=0.8)
            axes[0].plot(sd[column], linewidth=6, alpha=0.9)
            axes[0].plot(sd['curve'], linewidth=7, alpha=0.9)

            # axes[1].bar(
            #     [i for i in range(len(group)) if group['date'][i] >= infection_date],
            #     1000000,
            #     color='gray', width=1, alpha=0.15,
            # )
            # axes[1].plot(distances, linewidth=6, alpha=1)
            axes[1].plot(np.array(sparced_distances) / max(sparced_distances), linewidth=6, alpha=1)
            axes[1].plot(differnces, linewidth=6, alpha=1)

            axes[0].set_title(
                f'Windowed distance between time series and fitted polynomial\n'
                f'Mouse - {name}, Feature - {column}, Poly.Degree - {poly_degree},\n'
                f'Distance Window - {distance_window_hours} hr.',
            )
            # axes[0].legend([
            #     'cleared',
            #     'trend',
            #     'poly curve',
            # ], loc=1)
            # axes[0].set_xticks(list(zip(*dates))[0])
            # axes[0].set_xticklabels(list(zip(*dates))[1], rotation=30)
            # axes[0].set_ylim([0.95*series.min(), 1.02*series.max()])
            #
            # axes[1].legend([
            #     'distance',
            # ], loc=1)
            # axes[1].set_xticks(list(zip(*dates))[0])
            # axes[1].set_xticklabels(list(zip(*dates))[1], rotation=30)
            # axes[1].set_ylim([0.95*min(distances), 1.02*max(distances)])

            plt.savefig(f'plots/{name}_{column}.png')
            plt.close('all')

        pd.DataFrame(mice_distances).to_csv(f'{name}_distances.csv', index=False)
