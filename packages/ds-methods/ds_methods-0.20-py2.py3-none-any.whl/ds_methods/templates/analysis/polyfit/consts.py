import numpy as np
from datetime import datetime
import matplotlib.cm as cm


# POLYFIT
INTERPOLATION_SPARCING = 6 * 15
INFECTION_DATE = datetime(2020, 11, 4, 12, 00, 00)
RESAMPLE_MINUTES = 4
POINTS_PER_DAY = 24 * 60 // RESAMPLE_MINUTES
COLUMNS = ['area', 'size', 'temperature', 'speed', 'rotation', 'x_center', 'y_center', 'x_head', 'y_head']
MICE_NAMES = ['25', '26', '27', '31', '32']

# FFT
N_TOP_FFT_FREQUENCIES = 5
FFT_COLORS = cm.rainbow(np.linspace(0, 1, N_TOP_FFT_FREQUENCIES))
FFT_WINDOW_DAYS = 1
