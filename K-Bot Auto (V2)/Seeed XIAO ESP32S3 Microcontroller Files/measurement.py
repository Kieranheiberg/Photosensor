import board
import analogio
import digitalio
import time
import board

debug = False

#global variables
VCC = None
OD_LED = None

#print(dir(board))


def get_voltage(pin, vref): #update if want to check vref value
    
    # Convert raw reading (0–65535) to voltage (0–vref)
    raw = read_average(pin)
    voltage = (raw * vref) / 65535
    voltage_truncated = round(voltage, 3) #theoretically accuarte to 3 decimal places with averaging pin read out value. Test??!
    print(f"🔢 Raw: {raw} | ⚡ Voltage: {voltage_truncated} V")
    
    time.sleep(0.01)
    
    return voltage_truncated

def read_average(pin, samples=50):
    total = 0
    for _ in range(samples): #_ means is notation for throwaway variable
        total += pin.value
        time.sleep(0.01)
    return total / samples


def initialize_vref(pin):
    raw = read_average(pin, samples=100)  # do a more accurate average on startup
    voltage = (raw * 3.3) / 65535  # assume 3.3V to start
    
    print(f"Initial voltage check: {voltage} V")
    
    if voltage > 3.3:
        print("Switching reference voltage to 5V")
        vref = 5.0
    else:
        print("Reference voltage set to 3.3 V")
        vref = 3.3
    
    print("")
    return vref
    
def turn_on(power):
    global VCC, OD_LED

    if power:
        # Initialize pins and turn ON
        VCC = digitalio.DigitalInOut(board.IO3)
        OD_LED = digitalio.DigitalInOut(board.IO7)

        VCC.direction = digitalio.Direction.OUTPUT
        OD_LED.direction = digitalio.Direction.OUTPUT

        VCC.value = True
        OD_LED.value = True
        
        return [OD_LED, VCC]

    else:
        # Turn off and deinitialize
        if VCC:
            VCC.deinit()
            VCC = None
        if OD_LED:
            OD_LED.deinit()
            OD_LED = None


if (debug):
    
    [_, lol] = turn_on(True) #dummy variables that return pins
    analog_pin = analogio.AnalogIn(board.IO4)  # pin 4 is analog
    vref = initialize_vref(analog_pin)
    
    for _ in range(10):
        get_voltage(analog_pin, vref)
        time.sleep(1)
    
    turn_on(False)
    
