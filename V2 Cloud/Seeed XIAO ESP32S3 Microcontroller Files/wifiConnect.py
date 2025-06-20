import wifi
from wifi_info import wifi_info
import sys

debug = "false"

def connect_to_wifi(CurrentNetwork):
    
    SSID = wifi_info[f"{CurrentNetwork}_SSID"]
    PW = wifi_info[f"{CurrentNetwork}_PASS"]
    try:
        print("🔌 Connecting to Wi-Fi...")
        wifi.radio.connect(SSID, PW, timeout = 20)
        if wifi.radio.connected:
            print("✅ Connected to Wi-Fi Network:", SSID)
            print("📶 IP Address:", wifi.radio.ipv4_address)
            print("")
            
    except Exception as e:
        print("❌ Connection failed:", e)
        response = input("Reattempt connection? (y/n): ").strip().lower()
        if response == 'y':
            connect_to_wifi(CurrentNetwork)
        else:
            print("⚠️ Connection aborted.")
            sys.exit()
            
            
def get_MAC():
    mac = wifi.radio.mac_address
    mac_str = ":".join("{:02X}".format(b) for b in mac)
    print("📡 MAC Address:", mac_str)

def checkConnection():
    return wifi.radio.connected

def scanNetworks():
    print("🔍 Scanning available networks...")
    networks = list(wifi.radio.start_scanning_networks())
    wifi.radio.stop_scanning_networks()

    for net in networks:
        print(f"📡 {net.ssid}")

if (debug == "true"):
    CurrentNetwork = "MPSK" #current options = [Standard, MPSK, Squak, Kieran]
    connect_to_wifi(CurrentNetwork)
    get_MAC()
