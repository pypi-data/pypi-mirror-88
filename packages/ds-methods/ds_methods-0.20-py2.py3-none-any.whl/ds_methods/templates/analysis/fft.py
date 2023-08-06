import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from scipy import fftpack

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import *


from ds_methods.templates.init_data import load_raw_data


def index_to_fraction(index):
    if index == 0:
        return 1

    return 0.75 * (index + 1)


infection_date = datetime(2020, 11, 4, 12, 00, 00)
n_frequencies = 2
colors = cm.rainbow(np.linspace(0, 1, n_frequencies))

fft_window_days = 2

data = load_raw_data()

period = 24 * 60 // 4


columns = ['area', 'size', 'temperature', 'speed']
for name, group in data.groupby('target'):
    if True:#name in ['27']:
        group = group.reset_index(drop=True)
        sd_group = SeasonalDecomposition({'period': period}).make(group)['data']

        numeric_part, other_part = DataFrameUtils.decompose(group)

        day_groups = Group({'time': 24}).make(group)['data']

        dates = []
        for day, day_group in day_groups:
            if len(day_group) == period:
                dates.append([day_group.index[0], day.date()])

        for column in columns:
            column_fft_main_frequencies = []
            ffts = []
            max_freq = 24 * fft_window_days
            for day in range(len(dates) - fft_window_days): #day_group in day_groups:
                day_group = group[day * period: (day + fft_window_days) * period]
                if len(day_group) == fft_window_days * period:
                    series = day_group[column].tolist()
                    Fs = 1 # times per 4 minutes
                    N = len(series)
                    t = np.arange(0, len(series), 1 / Fs)

                    y_fft = fftpack.fft(series)[1:]
                    fr = (Fs / 2 * np.linspace(0, 1, N // 2 + 1))[1:]

                    y_m = 2 / N * abs(y_fft[:len(fr)])

                    top_n_frequencies = y_m.argsort()[-n_frequencies:][::-1]
                    column_fft_main_frequencies.append((4 / (60 * fr[top_n_frequencies])).tolist())
                    ffts.append([fr[:40], y_m[:40]])

            _, ax = plt.subplots(3, figsize=(14, 18))

            ## period
            ax[0].bar(
                [i for i in range(len(group)) if group['date'][i] >= infection_date],
                max(group[column]),
                color='gray', width=1, alpha=0.15,
            )
            ax[0].plot(group[column], linewidth=0.9, color='orange', alpha=0.8)
            ax[0].plot(sd_group[column], linewidth=3, color='darkred', alpha=0.8)

            for freq_index in range(n_frequencies):
                ax[1].bar(
                    range(1, len(column_fft_main_frequencies) + 1),
                    [freq[freq_index] for freq in column_fft_main_frequencies],
                    width=1.0 / index_to_fraction(freq_index), color=colors[freq_index],
                    align='edge', alpha=0.8 / index_to_fraction(freq_index), linewidth=3,
                )
            ax[1].bar(
                [i for i in range(1, len(column_fft_main_frequencies) + 1) if dates[i - 1][1] >= infection_date.date()],
                max_freq,
                color='gray', width=1, alpha=0.15, align='edge',
            )

            for fft in ffts:
                ax[2].plot(fft[0], fft[1], alpha=0.75, linewidth=0.9)
            for fft in ffts:
                ax[2].scatter([fft[0][np.argmax(fft[1])]], [np.max(fft[1])], alpha=0.9, s=100)

            ax[0].set_title(
                f'FFT Main Frequencies per day\n'
                f'Days Window {fft_window_days}, Mouse {name}, Feature {column}',
            )
            ax[0].set_xticks(list(zip(*dates))[0])
            ax[0].set_xticklabels(list(zip(*dates))[1], rotation=30)
            ax[0].set_ylabel(column)
            ax[0].set_ylim([group[column].min(), group[column].max()])
            ax[0].legend([f'raw for {column}', f'sd trend for {column}'], loc=1)

            ax[1].set_ylabel('frequency (hours)')
            ax[1].set_xticks(range(1, len(dates) + 1)[:len(column_fft_main_frequencies)])
            ax[1].set_xticklabels(list(zip(*dates))[1][:len(column_fft_main_frequencies)], rotation=30)
            # ax[1].set_yticks(range(1, 25))
            # ax[1].set_yticklabels(range(1, 25))
            ax[1].grid()
            ax[1].set_ylim([0, max_freq])
            ax[1].legend([f'top {freq + 1} frequency' for freq in range(n_frequencies)], loc=1)

            ax[2].set_ylabel('amplitude')
            ax[2].set_xlabel('frequency (hours)')
            ax[2].legend(list(zip(*dates))[1][:len(column_fft_main_frequencies)], loc=1)
            ax[2].set_xticks(ffts[0][0][::2])
            ax[2].set_xticklabels(np.round((4 / (60 * ffts[0][0]))[::2], 2), rotation=30)
            ax[2].grid()

            plt.savefig(f'plots/{name}_{column}.png')

            print(name, column)

            plt.close('all')
