# LED: White lead to ground. Red lead of LED connected to FIO7.
# Photosensor: Red lead to VS [Source voltage]. Silver/bare lead to Ground. White lead to AIN0 [output voltage].

import u3
import time
import csv
from datetime import datetime
import math

# Create a LabJack U3 object
try:
   dev = u3.U3()
except:
   print("Device not found")
   exit()

# Set FIO7 as a digital output and send 3.3V to the LED
dev.setDOState(7, 1) #Set FIO7 output to digital and high in one function; Sens power to LED red plugged into FIO7

OD = []
print("Start data collection")
interval = 0.1
duration = 5
sample_type = input("Enter the sample type (redrum, cbs, new): ")

validSample = False
while not validSample:
   if sample_type == 'redrum':
      ODConv = lambda sensor_output: -0.586 * math.log(sensor_output) + 0.2872 # uses redrum equation to convert voltage to OD
      validSample = True
   elif sample_type == 'cbs':
      ODConv = lambda sensor_output: -0.631 * math.log(sensor_output) + 0.2489 # uses cbs equation to convert voltage to OD
      validSample = True
   elif sample_type == 'new': #pointless have person write maually in script
      ODConv = ParseEquation(input("Enter Voltage to OD equation: "))
      validSample = True
   else:
      print("Enter a valid sample type")
      sample_type = input("Enter the sample type (redrum, cbs, new): ")

start_time = time.time()
while time.time() - start_time < duration:
   sensor_output = dev.getAIN(0)  # Read the voltage from AIN0
   OD_value = ODConv(sensor_output)
   current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
   OD.append((current_time, sample_type, OD_value)) # Adds time, sample type, and OD value to the Data list
   print("Time: ", current_time, " Type: ", sample_type, " Output (OD): ", OD_value)
   time.sleep(interval)

average_OD = sum([data[2] for data in OD]) / len(OD) # Calculates the average OD value
print("Average OD value: ", average_OD)

print("Save as CSV file? (y/n)")
if input() == "y":
    filename = input("Enter the file name: ")

    with open(filename, 'w', newline='') as file:
         out = csv.writer(file)
         out.writerow(["Time", "Sample Type", "OD Value"])
         out.writerows(OD)
else:
   print("Data not saved")

# LED off
dev.setDOState(7, 0)  # Low = 0 (0V) for FIO7 (turn off LED)

#If using LJContolPanel, Photosensor volatge out port should be set to AIN (analog Input) and LED Output port should be set 
# to DO (Digital Output) with Volateg box checked (sets state to 1 and ouputs voltage to LED)

def ParseEquation(equation):
   print("Equation parsing not set up yet :(")
