:: Navigate to the directory where your virtual environment and Python file are located
cd /d "C:\Users\kiera\OneDrive\Documents\GitHub\Photosensor"

:: Activate the virtual environment
call conda activate labjack

:: Run the Python script
python Export_csv.py

:: Deactivate the virtual environment after the script finishes
call conda deactivate

:: Prints message letting user know Export_csv.py program has finished running
echo Program finished

:: Leaves command prompt window open in case user wants to review printed sample data. Failsafe incase of unsuccessful save and need to see data
pause >nul
