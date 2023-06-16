import csv
import cv2
import matplotlib.pyplot as plt
from datetime import datetime

# Function to parse the timestamp string into a datetime object
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M")

# Function to generate graphs for a specific measurement (temperature, humidity, or soil moisture)
def generate_graph(data, measurement):
    # Create a dictionary to store data for each board ID
    board_data = {}

    # Iterate over the data and organize it based on board ID
    for row in data:
        boardid = row.get('board_id')
        print(boardid)
        value = float(row[measurement])
        timestamp = parse_timestamp(row['timestamp'])
        
        if boardid not in board_data:
            board_data[boardid] = {'timestamps': [], 'values': []}
        
        board_data[boardid]['timestamps'].append(timestamp)
        board_data[boardid]['values'].append(value)

    # Generate the graph
    plt.figure(figsize=(10, 6))
    for board_id, board in board_data.items():
        plt.plot(board['timestamps'], board['values'], label=boardid)

    plt.xlabel('Timestamp')
    plt.ylabel(measurement)
    plt.title(f'{measurement} Readings')
    plt.legend()
    plt.show()

# Read the CSV file
filename = 'C:/Users/Faizan Tabassum/Desktop/GardenWatch/sensor_data.csv'  # Replace with your CSV file name
data = []
with open(filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Generate graphs for temperature, humidity, and soil moisture
generate_graph(data, 'temperature')
generate_graph(data, 'humidity')
generate_graph(data, 'soil_moisture')
