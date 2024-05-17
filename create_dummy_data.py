import json
from datetime import datetime, timedelta

def generate_dummy_data(start_date, end_date):
    data = []
    current_date = start_date

    while current_date <= end_date:
        for hour in range(24):
            for minute in [0, 15, 30, 45]:  # Sampling 4 times per hour
                if hour < 8:
                    category = "Humid"
                    sensor_value = round(1.0 - (hour * 4 + minute / 15) * 0.00416667, 2)  # Gradual decrease from 1.00 to 0.67
                elif hour < 16:
                    category = "Dry"
                    sensor_value = round(0.66 - ((hour - 8) * 4 + minute / 15) * 0.00416667, 2)  # Gradual decrease from 0.66 to 0.33
                else:
                    category = "Very Dry"
                    sensor_value = round(0.33 - ((hour - 16) * 4 + minute / 15) * 0.00416667, 2)  # Gradual decrease from 0.33 to 0.00

                data_point = {
                    "year": current_date.year,
                    "month": current_date.month,
                    "day": current_date.day,
                    "hour": hour,
                    "minute": minute,
                    "second": 0,  # static second for simplicity
                    "category": category,
                    "sensor_value": sensor_value
                }
                data.append(data_point)
        current_date += timedelta(days=1)

    return data

# Define the date range
start_date = datetime(2024, 3, 1)
end_date = datetime(2024, 5, 14)

# Generate data
dummy_data = generate_dummy_data(start_date, end_date)

# Save to JSON file
with open('dummy_sensor_data.json', 'w') as file:
    json.dump(dummy_data, file, indent=4)

print("Data generated and saved successfully.")
