from machine import Timer, I2C, Pin, ADC
# wifi
import network
import wifi_utils
import wifi_config # name and password of network
import urequests  # Network Request Module
# Sensors
from dht12 import DHT12
from mq135 import MQ135
from gp2y1010au0f import GP2Y1010
# Display
import i2c_display


#TODO adapte period of timer and period of measure


# constants
PERIODE_MEASURES = 10

# Varibales
cnt = 0
readData = False


# Timer
tim = Timer(1)

def timer_handler(t):
    global cnt, readData
    cnt += 1
    if cnt % PERIODE_MEASURES == 0:
        readData = True

tim.init(period=100, mode=Timer.PERIODIC, callback=timer_handler)     # period in ms 

# Sensors
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor_dht12 = DHT12(i2c)
sensor_MQ = MQ135(36)
sensor_pm = GP2Y1010(25,34)


# Display
i2c_display.init_oled()


# Wifi 
def send_to_thingspeak(temp, humidity, co2, pm):

    # GET request
    url = f"{wifi_config.API_URL}?api_key={wifi_config.API_KEY}&field1={temp}&field2={humidity}&field3={co2}&field4={pm}"
    response = urequests.get(url)

    print(f"Entry # sent to ThingSpeak: {response.text}")
    response.close()

wifi = network.WLAN(network.STA_IF)     # Initialize the Wi-Fi interface in Station mode



try:
    temp, humidity = sensor_dht12.read_values()
    sensor_MQ.getCorrectedRZero(temp, humidity)
    while True:
        if readData:
            temp, humidity = sensor_dht12.read_values()
            co2 = sensor_MQ.getCorrectedPPM(temp, humidity)
            pm = sensor_pm.read_dust_density()
            
            wifi_utils.connect(wifi, wifi_config.SSID, wifi_config.PSWD)
            send_to_thingspeak(temp, humidity, co2, pm)
            wifi_utils.disconnect(wifi)

            i2c_display.update_oled(temp, humidity, co2, pm)
            readData = False
        
except KeyboardInterrupt:
    # This part runs when Ctrl+C is pressed
    print("Program stopped. Exiting...")

    # Optional cleanup code
    tim.deinit()  # Stop the timer
    wifi_utils.disconnect(wifi)

