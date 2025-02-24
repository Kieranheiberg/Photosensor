# LED: White lead to ground. Red lead of LED connected to FIO7.
# Photosensor: Red lead to VS [Source voltage]. Silver/bare lead to Ground. White lead to AIN0 [output voltage].

# If device not found make sure no other terminals are open. Labjack can only be accessed by one terminal at a time.
# If device not found, make sure the device is connected to the computer and the LabJack U3 driver is installed.

import u3
import time
import csv
from datetime import datetime
import math
import os
import json

"Still need to add ability to read header variables from csv file. Need to write logic to ensure function is valid (maybe convert from ln to math.log to make entry esasier"

# Create a LabJack U3 object
try:
    dev = u3.U3()
    connected = True
    print("Device found")
except:
    print("Device not found")
    connected = False
    print("Test Voltage set to 1") 
    Voltage = 1

# Set FIO7 as a digital output and send 3.3V to the LED
if connected: dev.setDOState(6, 1)  # Set FIO7 output to digital and high in one function; Sens power to LED red plugged into FIO7


#settings and initializations
interval = 0.1  # time between data collection
duration = 1  # length of time for data collection
Samples = []  # list to store samples


def main():
    sameType = False  # Initialize sameType variable
    input("Press Enter to start data collection. Use Ctrl+C to exit program at any time")

    while True:
        if not sameType:  # If sameType is Flase, ask for sample type
            sample_type = checkValidName()
        elif sameType:  # If sameType is True, use the same sample type
            sample_type = sample_type

        current_time = datetime.now().strftime("%H:%M:%S")  # Get current time in the format "HH:MM:SS"

        average_OD = measurement(sample_type)  # Collect data and calculate average OD
        print("Data collection complete\n")

        # Add sample to the Samples list
        Samples.append((current_time, sample_type, average_OD))

        print("Sample ", len(Samples))
        print("Time: ", current_time, " Type: ", sample_type, " Average OD value: ", average_OD)

        # Ask if user wants to take another sample
        continueLoop = input("\nPress Enter for another sample [type 'exit' to finish. type 'new' to change type]")

        if (continueLoop) == "exit": #if user does not want to take another sample break loop
            break
        elif (continueLoop == "new"): #if user wants to change sample type, set sameType to no
            sameType = False
        else: #keeps sample type the same
            sameType = True
    
    # Ask if user wants to save the data to CSV
    print("Save as CSV file? (y/n)")
    if input() == "y":
        SaveData(Samples)
    else:
        print("Data not saved")

    # Turn off LED
    if connected: dev.setDOState(6, 0)  # Low = 0 (0V) for FIO6 (turn off LED)



def checkValidName():
    """Ensures the sample type entered is valid by reading from the Equations JSON file."""
    valid_types = load_equations().keys()
    name = input(f"Enter the sample type ({', '.join(valid_types)}): ")
    while name not in valid_types:
        if input("Sample type not found. New species type? (y/n)\n") == "y":
            new_equation(name)
            valid_types = load_equations().keys()
            name = input(f"Enter the sample type ({', '.join(valid_types)}): ")
        else:
            name = input(f"Enter the sample type ({', '.join(valid_types)}): ")
    return name


def measurement(sample_type):
   """Handles data collection and calculates average OD value."""
   print("Data collection in progress...")
   start_time = time.time()
   sample_count = 0
   Voltage = []

   while time.time() - start_time < duration:  # Collect data over the specified duration
      if connected: sensor_output = dev.getAIN(0)  # Read the voltage from AIN0
      else: sensor_output = 1 # Test voltage if device not connected
      Voltage.append(sensor_output)
      sample_count += 1
      time.sleep(interval)

   average_V = sum(Voltage) / len(Voltage)  # Calculate the average voltage
   OD = ConvtoOD(average_V, sample_type)  # Convert the average voltage to OD value using stored/equation
   return OD


def ConvtoOD(Voltage, sample_type): 
    """Convert sensor output to OD value based on sample type."""
    equations = load_equations()  # Load calibration equations from the JSON file

    equation = equations.get(sample_type)
    if not equation:
        new_equation(sample_type)  # Ask user to enter a new equation if the sample type is not found

    try:
        OD = eval(equation, {"math": math, "Voltage": Voltage})  # Evaluate the equation for OD calculation
    except Exception as e:
        print(f"Error in equation: {e}")
        OD = None

    return OD

def new_equation(sample_type):
    """Save new calibration equation to a JSON file."""
    equations = load_equations()  # Load calibration equations from the JSON file

    newEquation = input("Enter Voltage to OD equation: ")
    #Add check if equation is valid
    
    equations[sample_type] = newEquation  # Save new equation for the sample type
    save_equations(equations)  # Save updated equations to JSON file
    print("Equation saved")


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

def save_equations(equations):
    """Save calibration equations to a JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), 'Equations.json')
    with open(file_path, 'w') as file:
        json.dump(equations, file, indent=4)  # Write updated equations to JSON file


def SaveData(Samples):
    """Save data as a CSV file."""
    filename = input("Enter the file name: ")

    # Ensure the file name has ".csv" extension
    if not filename.endswith(".csv"):
        filename += ".csv"

    # Check if the file already exists
    file_exists = os.path.isfile(filename)
    if file_exists:
        print("File already exists. Data will be appended to the existing file.")

    with open(filename, 'a', newline='') as file:
        out = csv.writer(file)
        # Write header only if the file does not already exist
        if not file_exists:
            out.writerow(["Time", "Sample Type", "OD Value"])
        out.writerows(Samples)
        print("Data saved to", filename)

        # Open the created CSV file in Excel
        if input("Open file in Excel? (y/n)\n") == "y":
            try:
                os.startfile(filename)
            except Exception as e:
                print(f"Could not open file in Excel: {e}")
   

# Run the program
if __name__ == "__main__":
    main()
