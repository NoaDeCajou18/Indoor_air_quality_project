from machine import Timer, I2C, Pin
# wifi
import network
import wifi_utils
import config # name and password of network
import urequests  # Network Request Module
# Sensors
from dht12 import DHT12
from mq135 import MQ135
import gp2y1010au0f
# Display
import i2c_display
from gp2y1010_pwm import GP2Y1010

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
    if cnt % PERIODE_MEASURES == 0 :
        readData = True

tim.init(period=100, mode=Timer.PERIODIC, callback=timer_handler)     # period in ms 

# Sensors
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor_dht12 = DHT12(i2c)
myMQ = MQ135(36)
sensor_pm = GP2Y1010(adc_pin=34, led_pin=25) 

# Display
i2c_display.init_oled()


# Wifi
API_KEY = "IHK5I6MLU9OLLS9V" 
def send_to_thingspeak(temp, humidity,co2, pm):
    API_URL = "https://api.thingspeak.com/update"

    # GET request
    url = f"{API_URL}?api_key={API_KEY}&field1={temp}&field2={humidity}&field3={co2}&field4={pm}"
    response = urequests.get(url)

    print(f"Entry # sent to ThingSpeak: {response.text}")
    response.close()

wifi = network.WLAN(network.STA_IF)     # Initialize the Wi-Fi interface in Station mode



try:
    temp, humidity = sensor_dht12.read_values()
    myMQ.getCorrectedRZero(temp, humidity)
    while True:
        if readData:
            temp, humidity = sensor_dht12.read_values()
            co2 = myMQ.getCorrectedPPM(temp, humidity)
            v, pm  = gp2y1010au0f.read_gp2y1010()
            
            wifi_utils.connect(wifi, config.SSID, config.PSWD)
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

