import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from scipy import fftpack

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import *

from ds_methods.templates.analysis.polyfit.consts import *
from ds_methods.templates.analysis.polyfit.utils import *
from ds_methods.templates.analysis.polyfit.polyfit_daily_analysis import polyfit_dayli_analysis


def index_to_fraction(index):
    if index == 0:
        return 1

    return 0.75 * (index + 1)


data = polyfit_dayli_analysis(is_plot=False)

fft_dataframe = []
for name in data:
    for column in data[name]:
        dates = data[name][column]['dates']
        init_series = data[name][column]['series']
        sd = data[name][column]['sd']
        all_dates = data[name][column]['all_dates']
        polynomial_data = data[name][column]['polynomial_info']['data']
        polynomial_minus_trend = data[name][column]['polynomial_minus_trend']

        column_fft_main_frequencies = []
        ffts = []
        for day in range(len(dates) - FFT_WINDOW_DAYS + 1):
            day_group = polynomial_minus_trend[day * POINTS_PER_DAY: (day + FFT_WINDOW_DAYS) * POINTS_PER_DAY]
            if len(day_group) == FFT_WINDOW_DAYS * POINTS_PER_DAY:
                series = day_group.tolist()
                Fs = 1  # times per 4 minutes
                N = len(series)
                t = np.arange(0, len(series), 1 / Fs)

                y_fft = fftpack.fft(series)[1:]
                fr = (Fs / 2 * np.linspace(0, 1, N // 2 + 1))[1:]

                y_m = 2 / N * abs(y_fft[:len(fr)])

                top_n_frequencies = y_m.argsort()[-N_TOP_FFT_FREQUENCIES:][::-1]
                # column_fft_main_frequencies.append((4 / (60 * fr[top_n_frequencies])).tolist())
                column_fft_main_frequencies.append((N * fr[top_n_frequencies]).tolist())
                ffts.append([fr[:10], y_m[:10]])

        # max_freq = 24 * FFT_WINDOW_DAYS
        max_freq = np.array(column_fft_main_frequencies).max()# 24 * FFT_WINDOW_DAYS

        _, ax = plt.subplots(5, figsize=(14, 30))

        ## period
        ax[0].bar(
            [i for i in range(len(all_dates)) if all_dates[i] >= INFECTION_DATE],
            max(init_series),
            bottom=min(init_series),
            color='gray', width=1, alpha=0.15,
        )
        ax[0].plot(init_series, linewidth=1, color='darkred', alpha=0.8)
        ax[0].plot(sd, linewidth=3, alpha=0.8)
        ax[0].plot(polynomial_data, linewidth=4, alpha=0.8)

        ax[1].plot(sd, linewidth=3, color='darkred', alpha=0.8)
        ax[2].plot(polynomial_minus_trend, linewidth=3, color='darkred', alpha=0.8)

        for freq_index in range(N_TOP_FFT_FREQUENCIES):
            ax[3].plot(
                range(1, len(column_fft_main_frequencies) + 1),
                [freq[freq_index] for freq in column_fft_main_frequencies],
                # width=1.0 / index_to_fraction(freq_index),
                color=FFT_COLORS[freq_index],
                # align='edge',
                # alpha=0.8 / index_to_fraction(freq_index),
                linewidth=3,
            )
        ax[3].bar(
            [i for i in range(1, len(column_fft_main_frequencies) + 1) if dates[i - 1][1] >= INFECTION_DATE.date()],
            max_freq,
            color='gray', width=1, alpha=0.15, align='edge',
        )

        for fft in ffts:
            ax[4].plot(fft[0], fft[1], alpha=0.75, linewidth=0.9)
        for fft in ffts:
            ax[4].scatter([fft[0][np.argmax(fft[1])]], [np.max(fft[1])], alpha=0.9, s=100)

        ax[0].set_title(
            f'FFT Main Frequencies per day\n'
            f'Days Window {FFT_WINDOW_DAYS}, Mouse {name}, Feature {column}',
        )
        ax[0].set_xticks(list(zip(*dates))[0])
        ax[0].set_xticklabels(list(zip(*dates))[1], rotation=30)
        ax[0].set_ylabel(column)
        ax[0].legend(['raw', 'trend', 'polynomial'])
        ax[0].set_ylim([min(init_series), max(init_series)])

        ax[1].legend(['trend'])
        ax[1].set_xticks([])

        ax[2].legend(['polynomial without trend'])
        ax[2].set_xticks([])

        ax[3].set_ylabel('frequency')
        ax[3].set_xticks(range(1, len(dates) + 1)[:len(column_fft_main_frequencies)])
        ax[3].set_xticklabels(list(zip(*dates))[1][:len(column_fft_main_frequencies)], rotation=30)
        # ax[3].set_yticks(range(1, 25))
        # ax[3].set_yticklabels(range(1, 25))
        ax[3].grid()
        ax[3].set_ylim([0, max_freq + 1])
        ax[3].legend([f'top {freq + 1} frequency' for freq in range(N_TOP_FFT_FREQUENCIES)], loc=1)

        ax[4].set_ylabel('amplitude')
        ax[4].set_xlabel('frequency (hours)')
        ax[4].legend(list(zip(*dates))[1][:len(column_fft_main_frequencies)], loc=1)
        ax[4].set_xticks(ffts[0][0][::2])
        ax[4].set_xticklabels(np.round((4 / (60 * ffts[0][0]))[::2], 2), rotation=30)
        ax[4].grid()

        plt.savefig(f'plots/{name}_{column}.png')

        print(name, column)

        plt.close('all')

        fft_dataframe += [
            {
                'mouse': name,
                'feature': column,
                'date': dates[i][1],
                **{
                    f'top_{freq + 1}_frequency': column_fft_main_frequencies[i][freq]
                    for freq in range(N_TOP_FFT_FREQUENCIES)
                }
            }
            for i in range(len(column_fft_main_frequencies))
        ]

pd.DataFrame(fft_dataframe).to_csv('ffts.csv', index=False)
