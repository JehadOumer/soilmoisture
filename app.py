from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime, timedelta
import sys

app = Flask(__name__)

# Command line argument for the JSON file, default to 'dummy_sensor_data.json', sensor_data.json for live sessions
json_file = sys.argv[1] if len(sys.argv) > 1 else 'dummy_sensor_data.json'


###parsing semi-json file to be json
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read().strip()
            if not file_content.startswith('[') or not file_content.endswith(']'):
                file_content = "[" + file_content.rstrip(',\n') + "]"
            data = json.loads(file_content)
        return data
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return []  # Return an empty list on error

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/current', methods=['GET'])
def current_data():
    data = load_json_data(json_file)
    return jsonify(data[-1] if data else {})

@app.route('/data/today', methods=['GET'])
def today_data():
    data = load_json_data(json_file)
    last_date = get_last_entry_date(data)
    today_data = [d for d in data if datetime(d['year'], d['month'], d['day']).date() == last_date]
    today_data_sorted = sorted(today_data, key=lambda x: (x['hour'], x['minute'], x['second']))
    return jsonify(today_data_sorted)

@app.route('/data/last7days', methods=['GET'])
def last_7_days_data():
    data = load_json_data(json_file)
    last_date = get_last_entry_date(data)
    date_7_days_ago = last_date - timedelta(days=7)
    last_7_days_data = [d for d in data if date_7_days_ago <= datetime(d['year'], d['month'], d['day']).date() <= last_date]
    last_7_days_data_sorted = sorted(last_7_days_data, key=lambda x: (x['year'], x['month'], x['day']))
    return jsonify(last_7_days_data_sorted)

@app.route('/data/custom_range', methods=['POST'])
def custom_range_data():
    data = load_json_data(json_file)
    start_date = request.json.get('start')
    end_date = request.json.get('end')
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    custom_data = [d for d in data if start_date <= datetime(d['year'], d['month'], d['day']).date() <= end_date]
    custom_data_sorted = sorted(custom_data, key=lambda x: (x['year'], x['month'], x['day'], x['hour'], x['minute'], x['second']))
    return jsonify(custom_data_sorted)

@app.route('/data/available_dates', methods=['GET'])
def available_dates():
    data = load_json_data(json_file)
    first_date, last_date = get_date_range(data)
    return jsonify({'min': first_date.strftime('%Y-%m-%d'), 'max': last_date.strftime('%Y-%m-%d')})

def get_last_entry_date(data):
    if data:
        last_entry = data[-1]
        return datetime(last_entry['year'], last_entry['month'], last_entry['day']).date()
    return None

def get_date_range(data):
    if data:
        first_date = datetime(data[0]['year'], data[0]['month'], data[0]['day'])
        last_date = datetime(data[-1]['year'], data[-1]['month'], data[-1]['day'])
        return first_date.date(), last_date.date()
    return None, None

if __name__ == '__main__':
    app.run(debug=True)
