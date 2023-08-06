import numpy as np
from matplotlib import pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import acf, pacf, plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling
from ds_methods.templates.init_data import load_raw_data

data = load_raw_data()

n_resample_minutes = 4
period = 24 * 60 // n_resample_minutes
distance_window = 4 * 60 // n_resample_minutes

print(data)

columns = ['area', 'size', 'temperature', 'speed']
for name, group in data.groupby('target'):
    if name in ['25', '26', '27', '31', '32']:
        group = group.reset_index(drop=True)
        # group = group[:4*period]
        numeric_part, other_part = DataFrameUtils.decompose(group, ['number', 'datetime'])

        day_groups = Group({'time': 24}).make(group)['data']

        dates = []
        for day, day_group in day_groups:
            if not day_group.empty:
                dates.append([day_group.index[0], day.date()])

        # dates = dates[:]
        # numeric_part = numeric_part.loc[:dates[-1][0]]
        # first_day = numeric_part.iloc[:period].diff().fillna(numeric_part.mean())
        # print(first_day)
        #
        # def diff_first_day(group):
        #     for column in group.columns:
        #         group[column] = group[column] - first_day[column]
        #
        #     return group
        #
        # group = Group({'time': 24})\
        #     .make(numeric_part)['data']\
        #     .apply(diff_first_day)

        # numeric_part = numeric_part.diff().dropna()

        # diff_level_1 = numeric_part.diff().dropna()
        # diff_level_period = diff_level_1.diff(period).dropna()

        for column in columns:
            a, confint_acf = acf(numeric_part[column], fft=True, nlags=period*2, alpha=.05)
            a, confint_acf = a[1:], confint_acf[1:]
            series = numeric_part[column]

            # distances = [None] * n_resample_minutes
            # for index in range(len(series) // distance_window):
            #     left_index = index * distance_window
            #     right_index = (index + 1) * distance_window
            #     distances += [(np.linalg.norm(series[left_index: right_index] - curve[left_index: right_index]))] * distance_window

            # sd_level_1 = seasonal_decompose(diff_level_1[column], period=period, extrapolate_trend=False)
            # sd_level_period = seasonal_decompose(diff_level_period[column], period=period, extrapolate_trend=False)
            _, axes = plt.subplots(2, figsize=(14, 12))

            # group[column].hist(ax=axes, alpha=0.75, bins=100)
            # diff_level_1[column].hist(ax=axes, alpha=0.75, bins=100)
            # diff_level_period[column].hist(ax=axes, alpha=0.75, bins=100)

            axes[0].plot(series, linewidth=1, alpha=1)
            # axes[0].plot(distances, linewidth=1, alpha=1)

            axes[1].plot(a)
            axes[1].fill_between(range(len(a)), confint_acf[:, 0] - a, confint_acf[:, 1] - a, alpha=.25)

            last_log = np.where(a >= confint_acf[:, 1] - a)[0][-1]
            print(name, column, last_log)

            axes[1].bar([last_log], 1, color='red')

            # axes.plot(group[column], linewidth=1, alpha=0.8)
            # axes.plot(diff_level_1[column], linewidth=1, alpha=0.8)
            # axes.plot(diff_level_period[column], linewidth=1, alpha=0.8)
            #
            axes[0].legend([
                'raw',
                'diff 1',
                'diff period',
            ])
            axes[0].set_xticks(list(zip(*dates))[0])
            axes[0].set_xticklabels(list(zip(*dates))[1], rotation=30)

            plt.savefig(f'plots/{name}_{column}.png')

            # plt.show()
