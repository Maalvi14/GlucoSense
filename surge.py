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

# Split the data into training and validation sets
split_index = int(0.8 * len(X))
X_train, X_val = X[:split_index], X[split_index:]
y_train, y_val = y[:split_index], y[split_index:]

# Reshape the data for LSTM input
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_val = np.reshape(X_val, (X_val.shape[0], X_val.shape[1], 1))

# Train the model
model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

# Predict on the validation set
y_pred = model.predict(X_val)

# Detect rapid changes in glucose levels
threshold = 0.5  # Adjust this threshold based on your data
rapid_changes = []
for i in range(len(y_pred)):
    if abs(y_pred[i] - y_val[i]) > threshold:
        rapid_changes.append((timestamps[i + window_size], y_val[i]))

# Group rapid changes by day and calculate average
rapid_changes_by_day = {}
for timestamp, glucose in rapid_changes:
    day = timestamp.date()
    if day in rapid_changes_by_day:
        rapid_changes_by_day[day].append(glucose)
    else:
        rapid_changes_by_day[day] = [glucose]

# Calculate average rapid changes per day
average_rapid_changes = {}
for day, changes in rapid_changes_by_day.items():
    average_rapid_changes[day] = np.mean(changes)

# Create a sorted list of days and their corresponding average rapid changes
sorted_days = sorted(average_rapid_changes.keys())
average_changes = [average_rapid_changes[day] for day in sorted_days]

# Plot the graph of average rapid changes per day
plt.plot(sorted_days, average_changes)
plt.xlabel('Day')
plt.ylabel('Average Rapid Changes')
plt.title('Average Rapid Changes in Glucose Levels per Day')
plt.xticks(rotation=45)
plt.show()