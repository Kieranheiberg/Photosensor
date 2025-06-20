# OD Sensor
Used simple electronics and 3D printed parts to make an optical density sensor for measuring optical density (OD) of anaerobic bacteria in test tubes. OD Sensor works by shining an LED through a 3D-printed tube holder to a Photosensor on the opposing side. Photosensor returns a voltage value that is proportional to the OD of the sample.
Photosensor functions by acting as variable resistor that responds to amount of light received.  
<div align="center">
Lots of light on sensor = lots of resistance = low voltage = high OD value.  <p></p>
Low light on photosensor = minimal resistance = high voltage = low OD value. <p>
</div>

## Project Libraries
All necessary Python libraries can be installed with the following command:
**<p align="center"> pip install -r requirements.txt </p>**  

root requirements.txt installs all libraries for V1 and V2  
requirements.txt in each respective version folder has the necessary libraries for that version.
The same command is valid for all versions just make sure directory is set to requirements.txt location before running it


## V1 Labjack
First version. Utilizes LabJack U3 data acquisition device (DAQ) to power photosensor and LED. Voltage from photosensor connected to analog port on Labjack DAQ. DAQ is connected to laptop running Python script (export_csv.py in V1 Labjack folder).
Export_csv.py has user specify which species is being measured and then polls voltage reading from Labjack DAQ. Species options pulled from Equations.json file that contains calibration equations to convert voltage to optical density for each bacteria species.

## V2 Cloud
Optimized version. Uses Seeed XIAO ESP32S3 microcontroller with built-in wifi and Bluetooth capabilities. Seeed has flexible pins that can be specified as digital or analog. LED and photosensor powered of pin set as digital output (3.3V). Voltage from photosensor read by pin set to analog input. Voltage values are uploaded to Thingspeak channel (free IoT platform run by MATLAB). Thingspeak channel has 4 fields.

Field 1 = Voltage values  
Field 2 = Max Num (number of measurements)  
Field 3 = Max Time (run time)  
Field 4 = tinterval (measurement time interval)     

Max Num, Max Time, and tinterval all set by external Python script (setExperimentalParameters.py in V2 Cloud folder). Code on Seeed device polls a voltage value every tinterval seconds until Max Time or Max Num is reached then LED will blink 4 times before turning off. Voltage values uploaded to Thingspeak field 1 in real time (include link to Thingspeak channel). downloadData.py (in V2 Cloud folder) downloads voltage data from Thingspeak channel, converts it to OD values (using Equations.json), and then formats it into an easy-to-read CSV file.

## Coming soon
Implementing orbital shaker (for gas exchange) and red LED array (to improve bacteria growth) to OD sensor for full autonomous functionality. Both plugged into to Adafruit IoT relay controlled by digital output pin on Seeed microcontroller. Seeed will manage timing so that LED array and orbital shaker will remain on until OD measurement wanted. Functionality/timing all managed via Seeed microcontroller and is as follows:

1. Seeed board will turn on IoT relay (and therefore LED array and orbital shaker)
2. Wait preset measurement interval time (tinterval in Thingspeak channel)
4. IoT relay turned off via Seeed pin set to digital output (and therefore turns off LED array and orbital shaker)
5. Measurement LED (for determining OD) turned on via Seeed pin set to digital output
6. Photosensor voltage value measured via Seeed pin set to analog input (measured voltage is proportional to OD of sample)
7. Voltage value uploaded to online ThingSpeak channel (field 1)
8. Seeed turns off measurement LED
9. Restarts orbital shaker and growth LED array by turning on IoT relay
10. Repeat until Max Num or Max Time reached (set by setExperimentalParameters.py or by hard-coding code.py in CIRCUITPY folder of Seeed)
11. LED blinks 4x times to indicate termination then turns off
    
