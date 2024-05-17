# soilmoisture
# Project Overview

This project aims to monitor soil moisture levels to ensure optimal plant watering. It uses an Arduino Uno to periodically check soil moisture and alerts users when watering is needed. The system includes a web interface to display real-time and historical moisture data.

## Components Used
- **Arduino Uno (ATmega328P)**: 1 unit
- **Soil Moisture Sensor (mh sensor series soil moisture)**: 1 unit
- **Red, Yellow, Green LEDs**: 1 unit each
- **Piezo Buzzer**: 1 unit
- **Resistors (100 Ohms)**: 4 units
- **Relay Switch (KEYES 5V Relay Module KY-019)**: 1 unit
- **Breadboard**: 1 unit
- **Jumper Wires**: Several

## Wiring Diagram
Refer to the provided breadboard wiring diagram for detailed connections.

## Running the Code

To run the project, use the `run_project.sh` script, which simplifies the process of starting the necessary components.

### Running the Project
1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/soil-moisture-monitor.git
    cd soil-moisture-monitor
    ```

2. **Run the project**:
    ```sh
    ./run_project.sh --data_source dummy_sensor_data.json --mode offline
    ```

### Command Line Arguments
- `--data_source`: Specifies the JSON file to use as the data source (default: `dummy_sensor_data.json`),  `sensor_data.json` is the file used for live experiments with the sensor
- `--mode`: Specifies the mode of operation (`live` for real-time data from the sensor or `offline` to use pre-recorded data).

### Description of Files
- `sensor_code.ino`: Arduino code for reading soil moisture levels and controlling indicators.
- `read_serial.py`: Script for reading serial data from the Arduino and saving it as JSON.
- `create_dummy_data.py`: Generates dummy sensor data for testing purposes.
- `app.py`: Flask application to serve the web interface and provide data endpoints.
- `index.html`: HTML file for the web dashboard interface.
- `charts.js`: JavaScript file for rendering charts on the web dashboard.
- `styles.css`: CSS file for styling the web interface.
- `sensor_data.json`: JSON file containing actual sensor data.
- `dummy_sensor_data.json`: Example JSON file with generated dummy data.
- `run_project.sh`: Shell script to run the project with specified parameters.

This project integrates hardware and software components to provide a soil moisture monitoring demo, accessible via a user-friendly web interface.
