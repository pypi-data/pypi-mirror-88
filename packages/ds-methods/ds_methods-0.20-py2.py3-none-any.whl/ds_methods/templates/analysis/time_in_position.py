import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.filters import *
from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling


from ds_methods.templates.init_data import load_raw_data


infection_date = datetime(2020, 11, 5, 00, 00, 00)
data = load_raw_data()

period = 24 * 60 // 4
window = 3


mouse_drinking_positions = {
    '25': {
        'x': [0.6, 1],
        'y': [0.4, 1],
    },
    '26': {
        'x': [0.6, 1],
        'y': [0.0, 0.6],
    },
    '27': {
        'x': [0.6, 1],
        'y': [0.0, 0.6],
    },
    '31': {
        'x': [0.0, 0.5],
        'y': [0.0, 0.6],
    },
    '32': {
        'x': [0.0, 0.5],
        'y': [0.4, 1],
    },
}

for name, group in data.groupby('target'):
    if True:#name in ['27']:
        group = group.reset_index(drop=True)
        numeric_part, other_part = DataFrameUtils.decompose(group)

        day_groups = Group({'time': 24}).make(group)['data']

        dates = []
        for day, day_group in day_groups:
            if len(day_group) == period:
                dates.append([day_group.index[0], day.date()])

        window_groups = Group({'time': window}).make(group)['data']
        times = {}
        for time, window_group in window_groups:
            (x_left, x_right) = mouse_drinking_positions[name]['x']
            (y_top, y_bottom) = mouse_drinking_positions[name]['y']
            filtered_rows = FilterByFeaturesValues({
                'x_center__gte': x_left,
                'x_center__lte': x_right,
                'y_center__gte': y_top,
                'y_center__lte': y_bottom,
            }).make(window_group)['data']

            times[time] = len(filtered_rows) * 4

        _, ax = plt.subplots(1, figsize=(16, 10))

        ax.bar(
            [i for i in range(len(list(times.values()))) if list(times.keys())[i] >= infection_date],
            max(times.values()),
            color='gray', width=1, alpha=0.15,
        )
        ax.bar(
            range(len(list(times.values()))),
            times.values(),
            color='orange', width=1, alpha=0.9,
        )

        ax.set_title(f'Time in drinking position\nMouse - {name}, Window time - {window} hours')
        ax.set_xticks(range(len(list(times.keys())))[::4])
        ax.set_xticklabels(list(times.keys())[::4], rotation=30)
        ax.set_ylabel('time (minutes)')

        ax.set_ylim([0, max(times.values())])

        plt.savefig(f'plots/{name}.png')

        plt.close('all')
