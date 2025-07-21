import numpy as np
import matplotlib.pyplot as plt

import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

# --- 1. Data Preparation ---
# Interval (minutes)
intervals = np.array([1, 2, 10, 30])
# Operating Time (hours, minutes)
durations_h = np.array([30, 30, 33, 31])
durations_m = np.array([8, 57, 19, 32])

# Convert all time units to minutes
total_minutes = durations_h * 60 + durations_m

# --- 2. Data Transformation for Linear Regression ---
# y = 1 / Operating Time
# x = 1 / Interval
x = 1 / intervals
y = 1 / total_minutes

# --- 3. Model Fitting (using numpy.polyfit) ---

# Case 1: Using all data
# np.polyfit(x, y, 1) returns coefficients [slope_all, intercept_all]
slope_all, intercept_all = np.polyfit(x, y, 1)

# The ratio E_dyn / P_stat has units of minutes and is calculated from slope / intercept
ratio_val_all = slope_all / intercept_all
# The dimensionless power ratio (avg dynamic power per min / static power)
power_ratio_all = 1 / (1 / ratio_val_all)


# Case 2: Excluding the suspicious outlier (the last data point)
x_filtered = x[:-1]
y_filtered = y[:-1]
slope_filtered, intercept_filtered = np.polyfit(x_filtered, y_filtered, 1)
ratio_val_filtered = slope_filtered / intercept_filtered
power_ratio_filtered = 1 / (1 / ratio_val_filtered)


# --- 4. Plotting ---
plt.figure(figsize=(12, 6))
x_fit = np.linspace(0, 1.1, 100)
y_fit_all = slope_all * x_fit + intercept_all

# Plot 2: Outlier Removed
ax = plt.gca()
ax.tick_params(which='minor', direction='in')
ax.tick_params(which='major', length=5, direction='in')
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
plt.scatter(x_filtered, y_filtered, color='blue', label='Data')
plt.scatter(x[-1], y[-1], color='gray', marker='x', s=100, label='Excluded (30 min)')
y_fit_filtered = slope_filtered * x_fit + intercept_filtered
ax.plot(x_fit, y_fit_filtered, color='green', linestyle='--', label=f'Regression Line')
ax.set_xlabel('1 / Interval (1/min)')
ax.set_ylabel('1 / Operation Time (1/min)')
ax.set_xlim(0, max(x) * 1.1)
ax.set_ylim(0, max(y) * 1.1)

plt.grid(True)
plt.legend(fontsize=15)
plt.show()

# --- 5. Printing Results ---
print("--- Analysis Results ---")
print(f"Excluding the outlier, the Dynamic:Static power ratio is approx. 1 : {power_ratio_filtered:.4f}")