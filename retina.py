import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# Define the LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(None, 1)),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Load and preprocess the data
data = pd.read_csv('data.csv')
glucose_levels = data['glucose_levels'].values
timestamps = pd.to_datetime(data['timestamps'])

# Normalize the glucose levels
glucose_levels = (glucose_levels - np.mean(glucose_levels)) / np.std(glucose_levels)

# Prepare the training data
window_size = 10  # Number of previous glucose levels to consider
X = []
y = []
for i in range(window_size, len(glucose_levels)):
    X.append(glucose_levels[i - window_size:i])
    y.append(glucose_levels[i])
X = np.array(X)
y = np.array(y)

# Reshape the data for LSTM input
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Train the model
model.fit(X, y, epochs=10)

# Predict on the entire dataset
y_pred = model.predict(X)

# Detect rapid changes in glucose levels
threshold = 0.5  # Adjust this threshold based on your data
rapid_changes = []
for i in range(len(y_pred)):
    if abs(y_pred[i] - y[i]) > threshold:
        rapid_changes.append((timestamps[i + window_size], y[i]))

# Group rapid changes by time of day and calculate average
rapid_changes_by_time = {}
for timestamp, glucose in rapid_changes:
    time = timestamp.time()
    if time in rapid_changes_by_time:
        rapid_changes_by_time[time].append(glucose)
    else:
        rapid_changes_by_time[time] = [glucose]

# Calculate average rapid changes per time of day
average_rapid_changes = {}
for time, changes in rapid_changes_by_time.items():
    average_rapid_changes[time] = np.mean(changes)

# Create lists of times and average rapid changes
times = [str(time) for time in sorted(average_rapid_changes.keys())]
average_changes = [average_rapid_changes.get(time, 0) for time in times]

# Plot the graph of average rapid changes per time of day
fig, ax = plt.subplots()
ax.plot(times, average_changes)
ax.set_xlabel('Time of Day')
ax.set_ylabel('Real Data - Predicted Data Threshold')
ax.set_title('Average Rapid Changes in Glucose Levels by Time of Day')
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
plt.xticks(rotation=45)
plt.show()
