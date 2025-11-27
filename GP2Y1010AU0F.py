from machine import ADC
from hw_config import PwmLed
import time

class GP2Y1010:
    def __init__(self, adc_pin=34, led_pin=25):
        # ADC pour la sortie du capteur
        self.adc = ADC(adc_pin)
        self.adc.atten(ADC.ATTN_11DB)
        # LED IR via PWM
        self.led = PwmLed(led_pin, frequency=100)  # 100 Hz → cycle = 10 ms
        # Duty cycle correspondant à 0.32 ms / 10 ms
        self.duty_percent = 3.2  

    def read(self):
        # Pulse LED IR
        self.led.on(self.duty_percent)   # LED ON pour 0.32 ms
        time.sleep_us(1000)               # 0.32 ms

        # Convertir ADC en voltage et poussière
        voltage = val * 3.3 / 4095
        dust = max((voltage - 0.9) * 200, 0)
        return voltage, dust

    def deinit(self):
        self.led.off()

