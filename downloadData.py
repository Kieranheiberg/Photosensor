import requests
from config import thingspeak_info  # Custom config file with your API key
import json
import os
import math
import csv
import time
from datetime import datetime
import pytz


def downloadData():
    channel_id = thingspeak_info['Channel_ID']  # replace with your channel ID
    url = f'https://thingspeak.com/channels/{channel_id}/feeds.csv'

    response = requests.get(url)

    if response.status_code == 200:
        with open('thingspeak_data.csv', 'wb') as f:
            f.write(response.content)
        print("CSV data downloaded successfully!")
    else: 
        print(f"Failed to download data. Status code: {response.status_code}")
        
def load_equations():
    """Load calibration equations from a JSON file."""
    try:
        # Use a relative path to ensure the file is found in the same folder
        file_path = os.path.join(os.path.dirname(__file__), 'Equations.json')
        with open(file_path, 'r') as file:
            return json.load(file)  # Load the JSON data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}  # Return empty dictionary if the file does not exist
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return {}

def ConvtoOD(Voltage, sample_type): 
    """Convert sensor output to OD value based on sample type."""
    equations = load_equations()  # Load calibration equations from the JSON file
    equation = equations.get(sample_type)

    try:
        #print(f"Evaluating OD with Voltage = {Voltage}, equation = {equation}")
        OD = eval(equation, {"math": math, "Voltage": Voltage})  # Evaluate the equation for OD calculation
    except Exception as e:
        #print(f"Error in equation for Voltage={Voltage}: {e}")
        OD = 0

    return OD

def formatCSV(sampleType):
    utc = pytz.utc
    pst = pytz.timezone("US/Pacific")

    with open('thingspeak_data.csv', 'r', newline='') as f:
        reader = list(csv.reader(f))
        header = reader[0]
        data_rows = reader[1:]

    idx_maxnum = 3
    idx_maxtime = 4
    idx_timeinterval = 5

    def last_non_empty(col_idx):
        for row in reversed(data_rows):
            if len(row) > col_idx and row[col_idx].strip():
                return row[col_idx].strip()
        return ''

    maxnum_val = last_non_empty(idx_maxnum)
    maxtime_val = last_non_empty(idx_maxtime)
    timeinterval_val = last_non_empty(idx_timeinterval)

    metadata_values = [
        f"Sample Type: {sampleType}",
        f"Max Number: {maxnum_val}",
        f"Max Time [min]: {maxtime_val}",
        f"Time Interval [s]: {timeinterval_val}"
    ]

    output_rows = []

    # First row: Header + first metadata
    data_header = ['Created at', 'Entry Number', 'Voltage [V]', 'OD']
    output_rows.append(data_header + ['', 'Parameters'])

    for i, row in enumerate(data_rows[:len(metadata_values)]):
        try:
            # Convert timestamp
            timestamp_str = row[0].replace(" UTC", "").strip()
            utc_dt = utc.localize(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
            pst_dt = utc_dt.astimezone(pst)
            created_at = pst_dt.strftime("%Y-%m-%d %H:%M:%S")

            entry_number = row[1] if len(row) > 1 else ''
            voltage_str = row[2].strip() if len(row) > 2 else ''
            voltage = float(voltage_str) if voltage_str else ''
            od_value = ConvtoOD(voltage, sampleType) if voltage_str else ''

            data_line = [created_at, entry_number, voltage_str, str(od_value)]
        except Exception as e:
            print(f"Error processing row {i}: {e}")
            data_line = row[:4]

        # Append metadata in column 6 only for the first 4 rows
        data_line += [''] * (5 - len(data_line)) + [metadata_values[i]]
        output_rows.append(data_line)

    # Process remaining rows (if any), no more metadata
    for row in data_rows[len(metadata_values):]:
        try:
            timestamp_str = row[0].replace(" UTC", "").strip()
            utc_dt = utc.localize(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
            pst_dt = utc_dt.astimezone(pst)
            created_at = pst_dt.strftime("%Y-%m-%d %H:%M:%S")

            entry_number = row[1] if len(row) > 1 else ''
            voltage_str = row[2].strip() if len(row) > 2 else ''
            voltage = float(voltage_str) if voltage_str else ''
            od_value = ConvtoOD(voltage, sampleType) if voltage_str else ''

            new_row = [created_at, entry_number, voltage_str, str(od_value)]
        except Exception as e:
            print(f"Error processing row: {e}")
            new_row = row[:4]

        output_rows.append(new_row)

    with open('thingspeak_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)
        
def openFile():
    # Open the created CSV file in Excel
    filename = "thingspeak_data.csv"
    if input("Open file in Excel? (y/n)") == "y":
        try:
            os.startfile(filename)
        except Exception as e:
            print(f"Could not open file in Excel: {e}")


downloadData()
valid_types = load_equations().keys()
sampleType = input(f"Enter the measured sample type ({', '.join(valid_types)}): ")
formatCSV(sampleType)
openFile()




