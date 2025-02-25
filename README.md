## Photosensor

# Config
1. Download RunPhotosensor.bat, Export_csv.py, Equations.json
2. Export_csv.py and Equations.json need to be in same file. RunPhotosensor can exist anyway         [Suggested on desktop]
3. Create conda virtual enviroment named labjack
4. Ensure LabJackPython package is installed to virtual enviroment.         [Run 'pip install LabJack' to install]
5. Change directory in RunPhotosensor.bat to where Export_csv and Equations are saved

# Sensor Setup
From LED: Red in FIO6, white in GND and make sure screw terminal is tight. 
From Photosensor:VCC wire goes to VS, GND goes to GND, and OUT goes to AIN0        [update with colors of wires. Should be in order and not twisted]

# Running
either:
- Run program by executing RunPhotosensor.bat   [Need to edit .bat file and change file dircetory to folder of Export_csv.py first. Double click on file to execute]
  
- Run following in command prompt:   ['>' indicates command prompt code]
   >conda activate labjack          [Should now see '(labjack)' in front of prompt. Only needed if using a virtual enviroment]
   >cd 'Export_csv directory'   [Folder where Export_csv.py and Equations.json are saved]
   >python Export_csv.py

# Troubleshooting
If seeing 'device not found. Test Voltage set to 1' LabJack device is not plugged into computer properly. Program will still run by wont give readings. Deesigned for running code without device nearby
If RunPhotosensor.bat not working, open in notepad and make sure "CD 'file dricetory'" is set to folder where Export_csv.py and Equations.json are saved

