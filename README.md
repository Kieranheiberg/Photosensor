# OD Sensor
Used simple electronics and 3D printed parts to make an optical density sensor for measuring optical denisty (OD) of anaerobic bacteria in test tubes. OD Sensor works by shining an LED through a 3D-printed tube holder to a Photosensor on the opposing side. Photosensor returns a voltage value that is proportional to the OD of the sample.
Photosensor functions by acting as variable resistor that responds to amount of light received.  
<div align="center">
Lots of light on sensor = lots of resistance = low voltage = high OD value.  <p></p>
Low light on photosensor = minimal resistance = high voltage = low OD value. <p>
</div>

## V1 Labjack
First version. Utilizes LabJack U3 data aquisition device (DAQ) to power photosensor and LED. Voltage from photosensor connected to analog port on Labjack DAQ. DAQ is connected to laptop running Python script (export_csv.py in V1 Labjack folder).
Export_csv.py has user specify which species is being measured and then polls voltage reading from Labjack DAQ. Species options pulled from Equations.json file that contains calibration equations to convert voltage to optical density for each bacteria species.

## V2 Cloud
Optimized version. Uses Seeed XIAO ESP32S3 microcontroller with built in wifi and bluetooth capabilities. Seeed has flexible pins that can be specified as digital or analog. LED and photosensor powered of pin set as digital output (3.3V).  

Voltage from photosensor read by pin set to analog input. Voltage values are uploaded to thingspeak channel (free IoT platform run by MATLAB). Thingspeak channel has 4 fields. Field 1 = Voltage values, Field 2 = Max Num (number of measurments), Field 3 = Max Time (run time),and Field 4 = tinterval (measurement time interval). Max Num, Max Time, and tinterval all set by external python script (setExperimentalParameters.py in V2 CLoud folder).  

Code on Seeed device polls a voltage value every tinterval seconds until Max Time or Max Num is reached then LED will blink 4 times before turning off. 
Voltage values uploaded to thingspeak field 1 in real time which appears under public channel tab (include link to thingspeak channel). downloadData (in V2 Cloud folder) downloads voltage data form thingspeak channel, converts it to OD values (using Equations.json), and then formats it into an easy to read csv file.

## Coming soon
Implementing orbital shaker (for gas exchange) and red LED array (to improve bacteria growth) to OD sensor for full autonomous functionality. Both plugged into to Adafruit IoT relay controlled by digital output pin on Seeed microcontroller. Seeed will manage timing so that LED array and orbital shaker will remain on until OD measurment wanted, then Seeed board will turn off IoT relay (and therefore LED array and orbital shaker), turn on measurement LED, get voltage value proportioanl to OD of sample, upload voltage value to online thingspeak channel, then restart orbital shaker and growth LED array.
