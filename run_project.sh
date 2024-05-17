#!/bin/bash

# Default values
DATA_SOURCE="dummy_sensor_data.json"  # default data source
MODE="offline"  # default mode

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --data_source) DATA_SOURCE="$2"; shift ;;
        --mode) MODE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Function to handle the termination of the script (Ctrl+C)
cleanup() {
    echo "Stopping all jobs..."
    [[ ! -z "$READ_SERIAL_PID" ]] && kill $READ_SERIAL_PID
    [[ ! -z "$APP_PID" ]] && kill $APP_PID
    exit 0
}

# Trap Ctrl+C (SIGINT) and call cleanup function
trap cleanup SIGINT

if [[ "$MODE" == "live" ]]; then
    # Run read_serial.py in the background and print its output
    echo "Starting read_serial.py in live mode..."
    python3 read_serial.py &
    READ_SERIAL_PID=$!
    echo "read_serial.py started with PID $READ_SERIAL_PID"
fi

# Optional: Delay before starting the next script
sleep 2

# Run app.py in the background with data source and print its output
echo "Starting app.py with data source $DATA_SOURCE..."
python3 app.py "$DATA_SOURCE" &
APP_PID=$!
echo "app.py started with PID $APP_PID, using data source: $DATA_SOURCE"

# Wait indefinitely until Ctrl+C is pressed
echo "Scripts are running. Press Ctrl+C to stop."
wait $READ_SERIAL_PID $APP_PID
