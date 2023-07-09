# GlucoSense
A simple Machine Learning algorithm in TensorFlow to detect and measure rapid glucose changes throughout the day.

This repository contains a TensorFlow program that detects rapid changes in glucose levels based on Freestyle Libre data. The program utilizes a Long Short-Term Memory (LSTM) network to analyze glucose levels and their corresponding timestamps to identify significant fluctuations.

## Requirements

- Python 3.x
- TensorFlow
- NumPy
- pandas
- matplotlib

## Installation

1. Make sure you have Python installed on your system. You can download the latest version of Python from the official website: https://www.python.org

2. Install the required Python packages by running the following command:
   pip install tensorflow numpy pandas matplotlib

## Usage

1. Clone this repository to your local machine or download the source code as a ZIP file.

2. Prepare your glucose data in CSV format. The CSV file should have two columns: `glucose_levels` and `timestamps`. Each row represents a data point, where the glucose level and timestamp are separated by a comma. Example:

glucose_levels,timestamps
120.5,2023-07-09 08:00:00
115.2,2023-07-09 08:15:00
110.8,2023-07-09 08:30:00
...


3. Save your glucose data as a CSV file named `data.csv` in the same directory as the Python script.

4. Open a terminal or command prompt, navigate to the directory containing the code, and run the following command:

python surge.py


5. The program will train an LSTM model on the provided data and detect rapid changes in glucose levels. The detected rapid changes will be printed to the console, and a graph of the average rapid changes per day will be displayed.

## Customization

- Adjust the `threshold` variable in the code to set the threshold for detecting rapid changes. Experiment with different values to find the most appropriate threshold for your data.
- Modify the `window_size` variable to change the number of previous glucose levels considered for analysis.
- Customize the graph appearance (e.g., labels, titles, formatting) using the `matplotlib` functions in the code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to contribute, open issues, or provide suggestions for improvement.
