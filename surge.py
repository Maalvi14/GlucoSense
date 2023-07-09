import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('data.csv')

# Extract glucose levels and timestamps
glucose_levels = data['glucose_levels']
timestamps = pd.to_datetime(data['timestamps'])

# Detect spikes in glucose levels
threshold = 1.5  # Adjust this threshold based on your data

spike_hours = []
spike_glucose_levels = []
for i in range(1, len(glucose_levels) - 1):
    if glucose_levels[i] - glucose_levels[i - 1] > threshold and glucose_levels[i] - glucose_levels[i + 1] > threshold:
        spike_hours.append(timestamps[i].hour)
        spike_glucose_levels.append(glucose_levels[i])

# Group spikes by hour
spikes_by_hour = {}
for hour, glucose in zip(spike_hours, spike_glucose_levels):
    if hour in spikes_by_hour:
        spikes_by_hour[hour].append(glucose)
    else:
        spikes_by_hour[hour] = [glucose]

# Calculate average spikes per hour
average_spikes = {}
for hour, spikes in spikes_by_hour.items():
    average_spikes[hour] = sum(spikes) / len(spikes)

# Create a list of hours in a day
hours_in_day = list(range(24))

# Create a list of average spike levels for each hour
average_spike_levels = [average_spikes.get(hour, 0) for hour in hours_in_day]

# Plot the average spike levels
plt.plot(hours_in_day, average_spike_levels, marker='o')
plt.xlabel('Hour of Day')
plt.ylabel('Average Glucose Level Spikes')
plt.title('Expected Average Glucose Level Spikes in a Normal Day')
plt.xticks(range(0, 24, 2))  # Set x-axis tick positions at every 2 hours
plt.grid(True, linestyle='--', alpha=0.5)  # Add grid lines
plt.show()
