:: Navigate to the directory where your virtual environment and Python file are located
cd "C:\Users\kiera\OneDrive\Documents\GitHub\Photosensor\K-Bot"

:: Run the Python script
python Export_csv.py

:: Prints message letting user know Export_csv.py program has finished running
echo Program finished

:: Leaves command prompt window open in case user wants to review printed sample data. Failsafe incase of unsuccessful save and need to see data
pause >nul
