import requests
import time
from config import thingspeak_info  # Custom config file with your API key

def upload_value(value, fieldNum):
    write_api_key = thingspeak_info["thingspeak_API_write"]
    write_url = f"https://api.thingspeak.com/update?api_key={write_api_key}&field{fieldNum}={value}"

    try:
        print(f"📤 Uploading to ThingSpeak field{fieldNum}: {value}")
        response = requests.get(write_url)
        print("✅ Uploaded!\n")
        response.close()
    except Exception as e:
        print("⚠️ Upload failed:", e)
      
def downloadData():
    channel_id = thingspeak_info['Channel_ID']  # replace with your channel ID
    url = f'https://thingspeak.com/channels/{channel_id}/feeds.csv'

    response = requests.get(url)

    if response.status_code == 200:
        with open('thingspeak_data.csv', 'wb') as f:
            f.write(response.content)
        print("CSV data downloaded successfully!")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")
        
        
#prompt for experiment parameters
MaxNumInput = input("Set max number of measurements? (NA voids) ")
MaxTimeInput = input("Set max run time in minutes? (NA voids) ")
tintervalInput = input("Set measuring time interval in seconds ")

MaxNum = 0
MaxTime = 0

if (MaxNumInput == 'NA'):
    MaxNum = 10000
else:
    MaxNum = int(MaxNumInput)
    
if (MaxTimeInput == 'NA'):
    MaxTime == 100000
else:
    MaxTime = int(MaxTimeInput)

#sets max to large number if voided so wont be reached
if (MaxNumInput == 'NA' and MaxTimeInput == 'NA'): #if both parameters voided then experiment runs for 5 min. Failsafe
    MaxTime = 5


#upload values to Thingspeak
upload_value(int(MaxNum), 2)
time.sleep(15)
upload_value(int(MaxTime), 3)
time.sleep(15)
upload_value(int(tintervalInput), 4)
time.sleep(1)

print("Parameters set")

