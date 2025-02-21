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

# Create a LabJack U3 object
try:
    dev = u3.U3()
except:
    print("Device not found")
    exit()

# Set FIO7 as a digital output and send 3.3V to the LED
dev.setDOState(6, 1)  # Set FIO7 output to digital and high in one function; Sens power to LED red plugged into FIO7


#settings and initializations
interval = 0.1  # time between data collection
duration = 5  # length of time for data collection
Samples = []  # list to store samples


def main():
    sameType = "n" #initialize sameType variable

    while True:
        # Get valid sample type input

      if sameType == "n": #if sameType is no, ask for sample type
         sample_type = checkValidName(input("Enter the sample type (redrum, cbs, new): "))

      elif sameType == "y": #if sameType is yes, use the same sample type
         sample_type = sample_type
      
      current_time = datetime.now().strftime("%H:%M:%S")  # Get current time in the format "HH:MM:SS"

      input("Press Enter to start data collection or Ctrl+C to exit")
      average_OD = measurement(sample_type)
      print("Data collection complete")
      
      # Add sample to the Samples list
      Samples.append((current_time, sample_type, average_OD))

      print("\nSample ", len(Samples))
      print("Time: ", current_time, " Type: ", sample_type, " Average OD value: ", average_OD)

      # Ask if user wants to take another sample
      if input("Another sample? (y/n)\n") == "n":
         break
      sameType = input("Same type? (y/n)\n")


    # Ask if user wants to save the data to CSV
    print("Save as CSV file? (y/n)")
    if input() == "y":
        SaveData(Samples)
    else:
        print("Data not saved")

    # LED off
    dev.setDOState(6, 0)  # Low = 0 (0V) for FIO6 (turn off LED)


def checkValidName(name):
    """Ensures the sample type entered is valid."""
    while name not in ['redrum', 'cbs', 'new']:
        print("Invalid sample type")
        name = input("Enter the sample type (redrum, cbs, new): ")
    return name


def measurement(sample_type):
   """Handles data collection and calculates average OD value."""
   print("Data collection in progress...")
   start_time = time.time()
   sample_count = 0
   Voltage = []

   while time.time() - start_time < duration:  # Subtracts current time from start time to get duration
      sensor_output = dev.getAIN(0)  # Read the voltage from AIN0
      Voltage.append(sensor_output)
      sample_count += 1
      time.sleep(interval)

   average_V = sum(Voltage) / (len(Voltage)+ 1)  # Calculate the average voltage
   OD = ConvtoOD(average_V, sample_type) # Converts the average voltage to OD value
   return OD


def ConvtoOD(Voltage, sample_type): #build out for external script capability
    """Convert sensor output to OD value based on sample type."""
    if sample_type == 'redrum':
        OD = -0.586 * math.log(Voltage) + 0.2872  # redrum equation
    elif sample_type == 'cbs':
        OD = -0.631 * math.log(Voltage) + 0.2489  # cbs equation
    elif sample_type == 'new':  # This will ask user to manually input a conversion equation
        equation = input("Enter Voltage to OD equation: ")
        OD = ParseEquation(equation)  # Implement a method to parse equations
    else:
        OD = None  # Fallback, not used but added for clarity
    return OD

def ParseEquation(equation):
    """Parse user-defined equations (not fully implemented)."""
    print("Equation parsing not set up yet :(")
    return None  # Or implement parsing logic here


def SaveData(Samples):
    """Save data as a CSV file."""
    filename = input("Enter the file name: ")

    # Ensure the file name has ".csv" extension
    if not filename.endswith(".csv"):
        filename += ".csv"

    with open(filename, 'w', newline='') as file:
        out = csv.writer(file)
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
