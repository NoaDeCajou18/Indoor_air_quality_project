from machine import Timer, I2C, Pin, PWM
# wifi
import network
import wifi_utils
import config # name and password of network
import urequests  # Network Request Module
# Sensors
from dht12 import DHT12
from mq135 import MQ135
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
    if cnt % PERIODE_MEASURES == 0 :
        readData = True

tim.init(period=100, mode=Timer.PERIODIC, callback=timer_handler)     # period in ms 

# Sensors
# Connect to the DHT12 sensor
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
sensor_dht12 = DHT12(i2c)
MyMQ = MQ135(36)

# GP2Y1010 PM2.5
adc_pm = ADC(Pin(34))
adc_pm.atten(ADC.ATTN_11DB)  # 0–3.3V
led_pwm = PWM(Pin(25), freq=1000, duty=0)  # PWM LED for dust sensor


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
    while True:
        if readData:
            temp, humidity = sensor_dht12.read_values()
            co2 = MyMQ.getCorrectedPPM(temp, humidity)
            pm  = 2 # TODO get data
            
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
