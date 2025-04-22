# LED: White lead to ground. Red lead of LED connected to FIO7.
# Photosensor: Red lead to VS [Source voltage]. Silver/bare lead to Ground. White lead to AIN0 [output voltage].


import u3
import time

# Create a LabJack U3 object
dev = u3.U3()

# Set FIO6 as a digital output and send 3.3V to the LED
dev.setDOState(6, 0) #Set FIO6 output to digital and high in one function; Sens power to LED red plugged into FIO7


# Read the photosensor output from AIN0 (connected to the sensor output)
try:
    while True:
        # Read the analog value from AIN0 (sensor output)
        sensor_output = dev.getAIN(0)  # Read the voltage from AIN0

        # Print the sensor output voltage 
        print(f"Sensor Output (Analog Voltage): {sensor_output:.5f} V") #:.5f rounds float to 5 decimal points [understand accuracy of device then change rounding]

        # Delay between readings for monitoring
        time.sleep(2)

except KeyboardInterrupt: #Use CTRl + C in terminal to stop
    print("Program interrupted by user.")

# LED off
dev.setDOState(6, 0)  # Low = 0 (0V) for FIO6 (turn off LED)


#If using LJContolPanel, Photosensor volatge out port should be set to AIN0 (analog Input) and LED Output port should be set to FI06
# to DO (Digital Output) with Volateg box checked (sets state to 1 and ouputs voltage to LED)
