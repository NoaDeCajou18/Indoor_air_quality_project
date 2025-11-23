from machine import Timer
# wifi
import network
import wifi_utils
import config # name and password of network
import urequests  # Network Request Module
# Sensors
from dht12.py import DHT12

#TODO adapte period of timer and period of measure


# constants
PERIODE_MEASURES = 500

# Varibales
cnt = 0
readData = False


# Timer
tim = Timer(1)

def timer_handler(t):
    global cnt, readData
    cnt += 1
    if cnt % PERIODE_MEASURES == 0 :
        readData = True

tim.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)     # period in ms 

# Sensors
# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor_dht12 = dht12.DHT12(i2c)



# Wifi
API_KEY = "" #TODO
def send_to_thingspeak(temp, humidity,co2, pm):
    API_URL = "https://api.thingspeak.com/update"

    # GET request
    url = f"{API_URL}?api_key={API_KEY}&field1={temp}&field2={humidity}&field3={co2}&field4={pm}"
    response = urequests.get(url)

    print(f"Entry # sent to ThingSpeak: {response.text}")
    response.close()

wifi = network.WLAN(network.STA_IF)     # Initialize the Wi-Fi interface in Station mode



try:
    while True:
        if readData:
            # TODO get data
            temp, humidity = sensor_dth12.read_values()
            co2, pm = getData()

            wifi_utils.connect(wifi, config.SSID, config.PSWD)
            send_to_thingspeak(temp, humidity, co2, pm)
            wifi_utils.disconnect(wifi)

            # TODO print data on OLED
            print(data)

            readData = False
        
except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    wifi_utils.disconnect(wifi)
