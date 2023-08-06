from matplotlib import pyplot as plt

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling

from ds_methods.methods.custom import TimeWarpingOnRegression

from ds_methods.templates.init_data import load_raw_data


data = load_raw_data(is_polynomials=True)

tw = Pipeline([
    # Group({
    #     'keys': ['target'],
    # }),
    # MovingAverage({
    #     'window': 60,
    # }),
    TimeWarpingOnRegression({}),
]).run(data)['data']

print(tw)
columns = ['area', 'size', 'temperature', 'speed']
for name, group in tw.groupby('target'):
    group = group.reset_index(drop=True)
    numeric_part, other_part = DataFrameUtils.decompose(group)

    day_groups = Group({'time': 24}).make(group)['data']

    dates = []
    for day, day_group in day_groups:
        if not day_group.empty:
            dates.append([day_group.index[0], day.date()])

    for column in columns:
        _, ax = plt.subplots(2, figsize=(14, 12))
        legends = []

        group.plot(y=column, ax=ax[0], linewidth=0.75, alpha=0.75)
        group.plot(y=f'{column}_regression', ax=ax[0], linewidth=1, alpha=0.8)
        group.plot(y=f'{column}_tw_distance', ax=ax[1], linewidth=3, alpha=0.85)

        legends += [
            f'Mouse: {name}, Feature: {column}',
            f'Mouse: {name}, Feature: {column}_regression',
        ]

        ax[0].set_title(f'Time-Warping Distance\nMouse - {name}, Feature - {column}')
        ax[0].set_xticks(list(zip(*dates))[0])
        ax[0].set_xticklabels(list(zip(*dates))[1], rotation=30)
        ax[0].set_ylabel(column)
        ax[0].set_xlabel('date')
        ax[0].legend(legends)

        ax[1].legend(f'Mouse: {name}, Feature: {column}_tw_distance')
        ax[1].set_xticks(list(zip(*dates))[0])
        ax[1].set_xticklabels(list(zip(*dates))[1], rotation=30)

        plt.savefig(f'plots/{name}_{column}.png')

        # plt.show()

tw.to_csv('tw_on_regression.csv', index=False)
