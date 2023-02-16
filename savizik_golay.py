import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

import matplotlib.pyplot as plt

#create a random time series
time_series = np.random.random(50)
time_series[time_series < 0.1] = np.nan
time_series = pd.Series(time_series)

print(time_series)

# interpolate missing data
time_series_interp = time_series.interpolate(method="linear")

print(time_series_interp)

# apply SavGol filter
time_series_savgol = savgol_filter(time_series_interp, window_length=7, polyorder=2)

print(time_series_savgol)

# plt.plot(time_series)
plt.plot(time_series_interp)
plt.plot(time_series_savgol)
plt.legend()
plt.show()