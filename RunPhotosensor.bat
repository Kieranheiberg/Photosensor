:: Navigate to the directory where your virtual environment and Python file are located
cd /d "C:\Users\kiera\OneDrive\Documents\GitHub\Photosensor"

:: Activate the virtual environment
call conda activate labjack

:: Run the Python script
python Export_csv.py

:: Deactivate the virtual environment after the script finishes
call conda deactivate

:: Exit the batch file
exit