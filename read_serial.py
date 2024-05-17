import serial
import json
from datetime import datetime
from serial.tools import list_ports

def find_arduino(vid_pid_tuple):
    # List all connected serial devices
    ports = list_ports.comports()
    #print(ports)
    for port in ports:
        if port.vid is not None and port.pid is not None: 
            if (port.vid, port.pid) == vid_pid_tuple: ##find port connected with arduino
                return port.device
    return None

# Setup the serial connection
arduino_vid_pid = (0x2341, 0x0043)  # VID and PID for Arduino Uno
arduino_port = find_arduino(arduino_vid_pid)
if arduino_port is None:
    print("Arduino not found. Please check your connection.")
    exit()


print("Arduino found at port", arduino_port)

ser = serial.Serial(arduino_port, 9600)

def process_data():
    with open('sensor_data.json', 'a') as file:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if "Average Moisture Level:" in line:
                try:
                    parts = line.split(': ')[1]
                    category, percentage = parts.split(', ')
                    
                    data = {
                        "year": datetime.now().year,
                        "month": datetime.now().month,
                        "day": datetime.now().day,
                        "hour": datetime.now().hour,
                        "minute": datetime.now().minute,
                        "second": datetime.now().second,
                        "category": category,
                        "sensor_value": float(percentage)
                    }

                    json.dump(data, file)
                    file.write(',\n')
                    file.flush()
                    print(data)

                except ValueError as e:
                    print("Error processing line:", line)
                    print(e)

if __name__ == "__main__":
    process_data()
