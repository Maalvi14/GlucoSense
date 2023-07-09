import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('data.csv')

# Extract glucose levels and timestamps
glucose_levels = data['glucose_levels']
timestamps = pd.to_datetime(data['timestamps'])

# Detect spikes in glucose levels
threshold = 1.5  # Adjust this threshold based on your data

spike_timestamps = []
spike_glucose_levels = []
for i in range(1, len(glucose_levels) - 1):
    if glucose_levels[i] - glucose_levels[i - 1] > threshold and glucose_levels[i] - glucose_levels[i + 1] > threshold:
        spike_timestamps.append(timestamps[i])
        spike_glucose_levels.append(glucose_levels[i])

# Plot the spikes in glucose levels
plt.plot(timestamps, glucose_levels, label='Glucose Levels')
plt.scatter(spike_timestamps, spike_glucose_levels, color='red', label='Spikes')
plt.xlabel('Timestamp')
plt.ylabel('Glucose Levels')
plt.title('Glucose Level Spikes')
plt.legend()
plt.xticks(rotation=45)
plt.show()
