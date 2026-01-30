# K-BOT Optical Density Sensor Documentation
K-BOT is custom built optical density densor ($OD$) for meausuring the $OD_{600}$ of bacteria grown anaerobically in either Hungate or Bulch tubes. K-BOT works by shining an LED through a 3D-printed tube holder to a Photosensor on the opposing side. 

## Operation
1. Ensure OD Sensor is plugged into lab laptop  USB port and you can see yellow LED inside the device is on. Full program is only avaliable on  lab laptop by platereaders
2. Double click **RunPhotosensor.bat** shortcut (On desktop of laptop)  
Terminal will output: 
```bash
python Export_csv.py

Device found
Press Enter to start data collection. Use Ctrl+C to exit program at any time
```
3. Press **Enter**. Terminal wil output:
```bash
Enter the sample type (redrum, cbs):
```
4. Place first sample into K-BOT tube holder
5. Type sample type name. Avaliable species listed in parenthesis. See **Add Species** section to add new sample types
6. Press **Enter** to collect OD value for current sample. Terminal will output:
```bash
Data collection in progress...
Data collection complete

Sample  1
Time:  15:21:28  Type:  redrum  Average OD value:  0.35783857457990265

Press Enter for another sample [type 'exit' to finish. type 'new' to change type]
```
7. Press **Enter** to collect another sample of the same type. Type **"new"** to change measured type (i.e change from measuirng rubrum to cbs)
8. Collect OD readings for all samples then type **"exit"** to end data collection
9. If you do not want to save date use **"n"** to end program  
**WARNING: COPY DOWN ALL NECESSARY VALUES BEFORE CLOSING TERMINAL WINDOW**
```bash
Program finished
```
10. To save all samples into CSV format use **"y"** and then enter file name. Do not use .csv in file name (i.e *JanResults* not *JanResults.csv*). File will be saved into PhotoSensor folder next to **RunPhotosensor.bat** shortcut on desktop
```bash
Save as CSV file? (y/n)
y
Enter the file name: JanResults
Data saved to JanResults.csv
Open file in Excel? (y/n)
n

Program finished
```


11. You can now safely close terminal window. Rerun **RunPhotosensor.bat** shortcut to start another round of data collection
 
## Add Species (Calibration Equations)
*Equations.json* is an editable file where all bacteria species calibration equations are stored dynamically. *Equations.json* is saved in photosensor folder on plate reader laptop desktop.  

To add a new species, open *Equations.json* and enter name followed by mathematical equation (in python code format) for new species. Example of full *Equations.json* file can be seen below:
```json
{
    "redrum": "-0.586 * math.log(Voltage) + 0.2872",
    "cbs": "-0.631 * math.log(Voltage) + 0.2489",
    "ln": "math.log(Voltage)"
}
```
New species should now be avaliable within *RunPhotosensor.bat*. Ensure not to leave comma after final entry as this will throw an error when trying to interpret file.

## Software Configuration
If you want to use K-BOT with a different computer follow the below steps:
1. Download *RunPhotosensor.bat*, *Export_csv.py*, *Equations.json* from: https://github.com/Kieranheiberg/Photosensor
2. *Export_csv.py* and *Equations.json* need to saved to the same folder. *RunPhotosensor.bat* can exist anyway         [Suggested on desktop]
3. Edit *RunPhotosensor.bat*  (Right click and select "Edit in Notepad") and change directory to folder containing *Export_csv.py* and *Equations.json* 
```bash
cd "C:\Users\kiera\OneDrive\Documents\GitHub\Photosensor\V1 Labjack" #Set to folder containing Export_csv.py and Equations.json
```
4. Create Conda virtual enviroment named labjack uaing terminal. Requires having Anaconda Navigator installed:
https://www.anaconda.com/products/navigator 
```bash
conda create --n labjack
```
5. Install LabJackPython package labjack virtual enviroment. 
```bash
conda activate labjack
(labjack) pip install LabjackPython
```



## Sensor Hardware Configuration
The OD value returned for each sample is calculated by taking a OD value every 0.1s interval for a total duration of 1s then finding average. The duration and interval of readings are set at 1s and 0.1s by default. 

These lengths can be modified by changing value of **interval** and **duration** variables at the top of *Export_csv.py* file. 
```python 
interval = 0.1 #seconds
duration = 1 #seconds
```

## Troubleshooting
Any questions regarding device opertaion or functionality can be directed to Kieran Heiberg  
Email: kieran.f.heiberg@hotmail.com  
Phone: +1 (425) 281-5745  
  
Diego Alba Burbano, Michael Guzman, Jackson Comes, Amanda Roberts, and Margaret Cook also have experience using device 
#### Hardware
1. If LED blinking, flickering or inconsistent:
  - Take off case and make sure wires connecting LED to red LabJack device is not being bent akwardly by the case
  - Verify wires connected correctly. Bold is LED terminal and [ ] is the LabJack device terminal name.
    - **Negative** ->  [FI06]
    - **Positive** -> [GND]
2. If receiving a constant OD value:
  - Ensure that the wires connecting to the photosensor are secure. If loose use screwdriver to tighten corresponding screw terminal.
  - Verify wires are connected correclty. Bold is photosensor port name and [ ] is the LabJack device terminal name.
    - **VCC** to [VS]
    - **GND** to [GND]
    - **OUT** to [AIN0]. 
  - Use LJControlPanel to see voltage values at each ports and veridy they are accurate (LJControlPanel is part of LabJack install package; Instructions for downloading in LabJack_U3_Documentation.docx in repository)


#### Software
1. If seeing:
```bash
'Device not found. Test Voltage set to 1':
```
  - LabJack device is not being found by the computer. Ensure device is plugged into computer properly. Program will still run but Voltage will be set to 1 V permanently rather then variable depending on OD of sample. Designed for troubleshooting and debugging code without device nearby.

2. If *RunPhotosensor.bat* not working, open in notepad and make sure file directory is set to folder containing *Export_csv.py* and *Equations.json*
```bash 
cd C:/'' #File Directory for Export_csv.py and Equations.json
```

3. If error with reading calibration equations:
- Check *Equations.json* to make sure no trailing comma after last calibration equation. This will will cause file to expect another equation that is not there and throw an error

