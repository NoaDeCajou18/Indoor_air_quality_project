from machine import Pin, ADC
import time

class GP2Y1010:

    def __init__(self, led_pin, adc_pin):
        self.led = Pin(led_pin, Pin.OUT)  # LED control pin
        self.adc = ADC(Pin(adc_pin))         # Analog input pin
        self.adc.width(ADC.WIDTH_12BIT) # 12-bit ADC resolution
        self.adc.atten(ADC.ATTN_11DB)   # Full-scale voltage (up to 3.3V)
        

    # Pin definitions
    

    def read_dust_density(self):
        self.led.value(1)
        time.sleep_us(280)  # LED pulse width
        raw_value = self.adc.read()
        time.sleep_us(40)
        self.led.value(0)
        
        
        # Convert raw ADC value to voltage (assuming 3.3V reference)
        voltage = raw_value * (3.3 / 4095.0)

        # Convert voltage to dust density (calibration formula)
        dust_density = max((voltage - 0.9) / 0.005, 0)  # µg/m³
        return dust_density, raw_value, voltage



def demo():
    gp2y1010_sensor = GP2Y1010(4,36)
    dust_density = gp2y1010_sensor.read_dust_density()
    print(f"Dust Density: {dust_density:.2f} µg/m³")
    time.sleep(1)