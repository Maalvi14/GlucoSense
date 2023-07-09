import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess the data
data = pd.read_csv('data.csv')
glucose_levels = data['glucose_levels'].values
timestamps = pd.to_datetime(data['timestamps'])

# Normalize the glucose levels
glucose_levels = (glucose_levels - np.mean(glucose_levels)) / np.std(glucose_levels)

# Detect spikes in glucose levels
threshold = 1.5  # Adjust this threshold based on your data

spike_times = []
for i in range(1, len(glucose_levels) - 1):
    if glucose_levels[i] - glucose_levels[i - 1] > threshold and glucose_levels[i] - glucose_levels[i + 1] > threshold:
        spike_times.append(timestamps[i])

# Create a plot to visualize the spikes
fig, ax = plt.subplots()
ax.plot(timestamps, glucose_levels, label='Glucose Levels')
ax.scatter(spike_times, [glucose_levels[timestamps.tolist().index(time)] for time in spike_times],
           color='red', label='Spikes')
ax.set_xlabel('Timestamp')
ax.set_ylabel('Glucose Levels')
ax.set_title('Glucose Level Spikes')
ax.legend()

# Format x-axis timestamps
fig.autofmt_xdate()

# Show the plot
plt.show()

# Print the times of spikes
if len(spike_times) > 0:
    print("Spikes in glucose levels were detected at the following times:")
    for time in spike_times:
        print(time.time())
else:
    print("No spikes in glucose levels were detected.")
