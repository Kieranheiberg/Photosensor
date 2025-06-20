# lib
import time
import wifi
import analogio
import digitalio
import board
import socketpool
import adafruit_requests
import ssl

# custom py files
import wifiConnect
import ThingspeakInterface
import measurement

# Parameters to change (editable remotely via ThingSpeak or locally)
default_tinterval = 10  # default: take measurement every 10 seconds
CurrentNetwork = "Squak"  # Possible SSIDs: [Standard, MPSK, Squak, Kieran]
measurementTime = 0.9

# Connect to Wi-Fi
wifiConnect.connect_to_wifi(CurrentNetwork)
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())


# Set parameters
onlineValues = True #Decides if want to set values via Thingspeak or have them hard coded
if (onlineValues):
    print("Most Recently Set Parameter Values:")
    maxNum = int(ThingspeakInterface.readParam(2, "maxNum", requests))
    maxTime = int(ThingspeakInterface.readParam(3, "maxTime [Min]", requests))
    tinterval_thingspeak = ThingspeakInterface.readParam(4, "time interval [s]", requests)

else:
    maxTime = 1 #minutes
    maxNum = 17

# Validate and adjust tinterval
if (onlineValues):
    tinterval = tinterval_thingspeak - measurementTime
    print(f"time interval [s]: {tinterval_thingspeak}")
else:
    print("Invalid or missing tinterval from ThingSpeak. Using default.")
    tinterval = default_tinterval - measurementTime
print("")  # spacer

# Turn on LED and photosensor
[OD_LED, VCC] = measurement.turn_on(True)
analog_pin = analogio.AnalogIn(board.IO4)  # pin 4 is analog

# Determine Vref
vref = measurement.initialize_vref(analog_pin)
time.sleep(0.5)

# Initialize counters
start_time = time.monotonic()
number = 0
elapsed = 0

# Measurement loop
while True:
    elapsed = time.monotonic() - start_time

    if number <= maxNum and elapsed < maxTime * 60:
        # Poll voltage and upload to ThingSpeak
        if number != -1:  # skip first erratic value
            print("Time elapsed [s]:", round(elapsed, 2))
            value = measurement.get_voltage(analog_pin, vref)
            uploaded_value = ThingspeakInterface.upload_value(value, requests)

            if value == uploaded_value:
                print(value, "successfully uploaded to ThingSpeak Channel\n")

        # Delay before next measurement
        if tinterval > 0:
            time.sleep(tinterval)
        else:
            print("Warning: tinterval too small or negative, skipping delay.")
        number += 1

    elif elapsed >= maxTime * 60 or number > maxNum:
        print(f"\nTerminating loop. Final number: {number}, elapsed: {round(elapsed,2)} s")
        print(f"Max allowed time: {maxTime * 60} s, MaxNum: {maxNum}")

        print("Blinking LED to indicate stop...")
        try:
            for _ in range(4):
                OD_LED.value = False
                time.sleep(0.5)
                OD_LED.value = True
                time.sleep(0.5)
        except Exception as e:
            print(f"LED blinking failed: {e}")
        break

    else:
        print("Failsafe triggered: unexpected loop exit.")
        break

# Turn off LED and sensor
measurement.turn_on(False)

