# OD Sensor
Used simple electronics and 3D printed parts to make an optical density sensor for measuring OD of anaerobic bacteria in Hungate tubes. OD Sensor works by shining an LED through a 3D-printed tube holder to a Photosensor on the opposing side. Photosensor returns a voltage value that is proportional to the OD of the sample

## Config
1. Download RunPhotosensor.bat, Export_csv.py, Equations.json
2. Export_csv.py and Equations.json need to be in same folder. RunPhotosensor can exist anyway         [Suggested on desktop]
3. Change directory in RunPhotosensor.bat to where Export_csv and Equations are saved
4. Create conda virtual enviroment named labjack 
5. Ensure LabJackPython package is installed to virtual enviroment.         [Run 'pip install LabJack' to install while in virtual enviroment]

The OD value returned for each sample is calculated by taking a OD value every 0.1s interval for a total duration of 1s then finding average. The duration and interval of readings are set at 1s and 0.1s by default. These lengths can be modified by changing value of 'interval' and 'duration' variables at the top of Export_csv.py file. Can be easily modified by editing code in notepad.  

## Sensor Setup
- From LED: Red in FIO6, white in GND and make sure screw terminal is tight. 
- From Photosensor:VCC wire goes to VS (green), GND goes to GND (blue), and OUT goes to AIN0 (purple)       [Wires should be in order and not twisted]

## Starting Export_csv.py
Either:
- Start program by executing RunPhotosensor.bat [Need to edit .bat file and change file directory to folder of Export_csv.py first. Double click on file to execute]
Or: 
- Run following in command prompt:   
   - 'conda activate labjack'          [Should now see '(labjack)' in front of prompt. Only needed if using a virtual enviroment]
   - 'cd "Export_csv directory" '   ["Export_csv directory" is directory to the folder where Export_csv.py and Equations.json are saved]
   - 'python Export_csv.py'
 
## Using Program
- Once Export_csv.py is running should see: 
  - 'Device Found. Press Enter to start data collection. Use Ctrl+C to exit program at any time'
- Pressing enter wil prompt for sample type. All existing sample types will be listed in the parenthesis.These names are pulled dircetly from the Equations.json file. 
- Enter name of current sample.
  - If you enter a new sample name, system will return 'Sample type not found. New species type? (y/n)'. If you type 'n' system will disregard enetred name and prompt for new one. If 'y' entered then will be asked 'Enter Voltage to OD equation:'. Equation must be entered using 'Voltage' variable (ex. '25*Voltage + 26') Math.log must be used for natural log function (ex. '0.988*Math.log(Voltage) + 0.674'). System will return 'Equation saved' if equation is successfully saved. You can view all exisitng calibration equations in Equations.json file.
  - Equations can be added or modified inside Equations.json as well and will auto update when running export_csv.py file. Suggested method for new calibration equations is to add it inside Equations.json file for easier editing and to see syntax of preexisiting valid calibration equations. 
- Once valid sample type entered, sensor will take reading and then print sample number, Time of reading, Type of sample, and Average OD value. These values are saved to an array so no need to copy them down.
- System will ask 'Press Enter for another sample [type 'exit' to finish. type 'new' to change type]'.
  - Pressing enter will record OD of another sample of same type as (if type is 'redrum' pressing enter will record OD value of another redrum sample).
  - Input of 'exit' will end sampling and take you to saving screen.
  - Input of 'new' will allow user to change sample type. 
- Exit prompt will ask user to save data as csv file. (WARNING: if you enter 'n' for saving data prompt there is no way to access collected data unless you manually scroll through prompts and record printed values for each sample. This is not recommended as it is much more intensive then saving as csv file). You can then enter name for the csv file.
  - Entering name of preexisting csv file will append data to the exisiting csv file.
- Csv file is saved to the same directory where Export_csv.py file is saved.

## Troubleshooting

#### Hardware
- If LED blinking or inconsistent take off case and make sure cable coming from LED is not being bent akwardly by the case
- If receiving a constant OD value ensure that the contacts coming from the photosensor are secure. Also ensure the wires are going from the correct terminal to the correct port on the LabJack device. It should be 'VCC' to [VS], 'GND' to [GND], and 'OUT' to [AIN0]. Where the name in '' is the photosensor port name and [] is the labjack terminal name.
  - Use LJControlPanel to see voltage values at the ports to check that readings are accurate (LJControlPanel is part of LabJack install package; Instructions for downloading in LabJack_U3_Documentation.docx in repository)

#### Software
- If seeing 'device not found. Test Voltage set to 1'. LabJack device is not being found by the computer. Ensure device is plugged into computer properly. Program will still run but Voltage will be set to 1 V permanently rather then variable depending on OD of sample. Designed for troubleshooting and debugging code without device nearby.
- If RunPhotosensor.bat not working, open in notepad and make sure "CD 'file directory'" is set to folder where Export_csv.py and Equations.json are saved
- If error surrounding processing json check to make sure no comma after last calibration equation in 'Equations.json' as this will will cause file to expect another equation that is not there throwing an error

