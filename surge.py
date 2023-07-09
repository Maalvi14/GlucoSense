import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess the data
data = pd.read_csv('data.csv')
glucose_levels = data['glucose_levels'].values
timestamps = pd.to_datetime(data['timestamps'], format='%d-%m-%Y %H:%M')

# Normalize the glucose levels
glucose_levels = (glucose_levels - np.mean(glucose_levels)) / np.std(glucose_levels)

# Detect spikes in glucose levels
threshold = 1.5  # Adjust this threshold based on your data

spike_times_by_day = {}
for i in range(1, len(glucose_levels) - 1):
    if glucose_levels[i] - glucose_levels[i - 1] > threshold and glucose_levels[i] - glucose_levels[i + 1] > threshold:
        day = timestamps[i].date()
        time = timestamps[i].time()
        if day in spike_times_by_day:
            spike_times_by_day[day].append(time)
        else:
            spike_times_by_day[day] = [time]

# Plot the spikes in glucose levels for each day
for day, spike_times in spike_times_by_day.items():
    day_timestamps = [timestamps[i] for i in range(len(timestamps)) if timestamps[i].date() == day]
    day_glucose_levels = [glucose_levels[i] for i in range(len(timestamps)) if timestamps[i].date() == day]

    fig, ax = plt.subplots()
    ax.plot(day_timestamps, day_glucose_levels, label='Glucose Levels')
    ax.scatter([timestamps[i] for i in range(len(timestamps)) if timestamps[i].time() in spike_times],
               [glucose_levels[i] for i in range(len(timestamps)) if timestamps[i].time() in spike_times],
               color='red', label='Spikes')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Glucose Levels')
    ax.set_title(f'Glucose Level Spikes - {day}')
    ax.legend()
    fig.autofmt_xdate()
    plt.show(block=True)

    print(f"Spikes in glucose levels for {day} were detected at the following times:")
    for time in spike_times:
        print(time)

    print("--------------------")

