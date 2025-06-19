# OD Sensor
Used simple electronics and 3D printed parts to make an optical density sensor for measuring optical denisty (OD) of anaerobic bacteria in test tubes. OD Sensor works by shining an LED through a 3D-printed tube holder to a Photosensor on the opposing side. Photosensor returns a voltage value that is proportional to the OD of the sample.
Photosensor functions by acting as variable resistor that responds to amount of light received. Lots of light on sensor = lots of resistance = low voltage = high OD value. Low light on photosensor = minimal resistance = high voltage = low OD value.

## V1 Labjack
First version. Utilizes LabJack U3 data aquisition device (DAQ) to power photosensor and LED. Voltage from photosensor connected to analog port on Labjack DAQ. DAQ is connected to laptop running Python script (export_csv.py in V1 Labjack folder).
Export_csv.py has user specify which species is being measured and then polls voltage reading from Labjack DAQ. Species options pulled from Equations.json file that contains calibration equations to convert voltage to optical density for each bacteria species.

## V2 Cloud
Optimized version. Uses Seeed XIAO ESP32S3 microcontroller with built in wifi and bluetooth capabilities. Seeed has flexible pins that can be specified as digital or analog. LED and photosensor powered of pin set as digital output (3.3V).
Voltage from photosensor read by pin set to analog input. Voltage values are uploaded to thingspeak channel (free IoT platform run by MATLAB). Thingspeak channel has 4 fields. Voltage values uploaded to field 1.
Max num (number of measurments) set to field 2, Max Time (run time) set to field 3, tinterval (measurement time interval) set to field 4. Max num, Max Time, and tinterval all set by external python script (setExperimentalParameters.py in V2 CLoud folder).
Seeed reads these values from thingspeak channel and then runs experiment based on those parameters. Code on Seeed device polls a voltage value every tinterval seconds until Max Time or Max Num is reached then LED will blink 4 times before turning off. 
Voltage values uploaded to thingspeak field 1 in real time and shows up under public channel tab (include link to thingspeak channel). 
