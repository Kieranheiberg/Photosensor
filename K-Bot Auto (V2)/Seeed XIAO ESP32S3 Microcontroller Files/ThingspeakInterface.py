from thingspeak_info import thingspeak_info
import socketpool
import adafruit_requests
import ssl
import wifiConnect
import wifi

debug = False

def upload_value(value, requests):
    if (wifi.radio.connected == "false"):
        print("not connected to wifi")
    
    # Prepare networking
    #pool = socketpool.SocketPool(wifi.radio)
    #requests = adafruit_requests.Session(pool, ssl.create_default_context())
    
    # Load API key and URL
    write_api_key = thingspeak_info["thingspeak_API_write"]
    

    # Input value from user
    #value = int(input("Enter Value: "))

    # Send data to ThingSpeak
    write_url = f"http://api.thingspeak.com/update?api_key={write_api_key}&field1={value}"
    write_response = requests.get(write_url)
    write_response.close()
    
    return value

def readParam(field_num, paramName, requests):
    #pool = socketpool.SocketPool(wifi.radio)
    #requests = adafruit_requests.Session(pool, ssl.create_default_context())
    
    read_api_key = thingspeak_info["thingspeak_API_read"]
    channel_id = thingspeak_info["Channel_ID"]
    num_retrieved = 50
    
    read_URL = f"https://api.thingspeak.com/channels/{channel_id}/fields/{field_num}.json?api_key={read_api_key}&results={num_retrieved}"
    read_response = requests.get(read_URL)
    
    data = read_response.json()  # Parse JSON
    read_response.close()        # Clean up the socket

    # Get the most recent feed entry
    feeds = data.get("feeds", [])
    for entry in reversed(feeds):
        val_str = entry.get(f"field{field_num}")
        if val_str is not None:
            try:
                val = float(val_str)
                if val != 0:
                    print(f"{paramName} = {val}")
                    return val
            except ValueError:
                # Skip invalid floats
                continue

    print("No non-zero values found.")
    return None
    
    
#If running this file independently for debugging/testing need to activate wifi and call a number
if (debug):
    network = "Squak"
    wifiConnect.connect_to_wifi(network)
    
    for i in range (2, 5, 1):
        field_num = i
        print (f"field {field_num}")
        readParam(field_num)
    #value = input("Enter value: ")
    #if (value == upload_value(value)):
        #print(value, "successfully uploaded to ThingSpeak Channel")
