import csv
import serial
from datetime import datetime

# TODO
# add a check to check if there is already headings, and if there is, don't print the board id
# temperature, and all that. just keep appending the values

# also make sure that empty values don't get added

def read_serial_data(ser):
    while True:
        line = ser.readline().decode().strip()
        if line.startswith('Board ID:'):
            board_id = int(line.split(': ')[1])
        elif line.startswith('Humidity value:'):
            humidity = int(line.split(': ')[1])
        elif line.startswith('Temperature value:'):
            temperature = int(line.split(': ')[1])
        elif line.startswith('Soil Moisture value:'):
            soil_moisture = int(line.split(': ')[1])
            return board_id, humidity, temperature, soil_moisture

# Serial port configuration
serial_port = 'COM3'  # Replace with your Arduino's serial port
baud_rate = 115200

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

# Create a CSV file and write the header
csv_file = open('sensor_data.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)
csv_file_read = open('sensor_data.csv', 'r')
File_Contents = csv_file_read.read()
if File_Contents == "":
    csv_writer.writerow(['board_id', 'humidity', 'temperature', 'soil_moisture','timestamp'])
else:
    pass

try:
    while True:
        # Read data from the serial monitor
        board_id, humidity, temperature, soil_moisture = read_serial_data(ser)
        nowtime = datetime.now()
        timestamp = nowtime.strftime("%Y/%m/%d %H:%M")
        
        # Write the data to the CSV file
        if board_id != '':
            csv_writer.writerow([board_id, humidity, temperature, soil_moisture, timestamp])
        else:
            pass
        csv_file.flush()  # Flush the buffer to ensure immediate write
        
except KeyboardInterrupt:
    # Close the serial port and CSV file on keyboard interrupt
    ser.close()
    csv_file.close()
