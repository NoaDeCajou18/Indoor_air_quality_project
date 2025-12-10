##
# @file gp2y1010.py
# @brief MicroPython driver for the Sharp GP2Y1010 optical dust sensor.
#
# This module provides a class for interfacing with the GP2Y1010 dust sensor.
# It handles LED pulsing, ADC measurement, and dust density calculation.
#
# Example:
# @code{.py}
# from gp2y1010 import GP2Y1010
# import time
#
# sensor = GP2Y1010(led_pin=4, adc_pin=36)
#
# while True:
#     dust = sensor.read_dust_density()
#     print("Dust Density: {:.2f} µg/m³".format(dust))
#     time.sleep(1)
# @endcode
#

from machine import Pin, ADC
import time

class GP2Y1010:
    ##
    # @class GP2Y1010
    # @brief Driver class for the Sharp GP2Y1010 dust sensor.
    #
    # This class manages the internal LED timing and ADC sampling required to
    # estimate particulate concentration from the sensor's analog voltage output.
    #

    ##
    # @brief Constructor for the GP2Y1010 dust sensor driver.
    #
    # Initializes the LED control pin and ADC input pin.
    #
    # @param led_pin GPIO pin number connected to the sensor LED control.
    # @param adc_pin GPIO pin number connected to the sensor analog output.
    #
    # @note ADC is configured for 12-bit width and 11 dB attenuation.
    #


    def __init__(self, led_pin, adc_pin):
        self.led = Pin(led_pin, Pin.OUT)  # LED control pin
        self.adc = ADC(Pin(adc_pin))         # Analog input pin
        self.adc.width(ADC.WIDTH_12BIT) # 12-bit ADC resolution
        self.adc.atten(ADC.ATTN_11DB)   # Full-scale voltage (up to 3.3V)
        

    ##
    # @brief Reads the dust density from the GP2Y1010 sensor.
    #
    # This function pulses the internal LED, performs an ADC measurement,
    # converts the reading to a voltage, and estimates dust density using a
    # simplified calibration equation.
    #
    # @return float Estimated dust density in µg/m³.
    #
    # @note Conversion formula:
    #       `dust_density = max((voltage - 0.4) / 0.05, 0)`
    #
    

    def read_dust_density(self):

        self.led.value(1)
        time.sleep_us(280)  # LED pulse width
        raw_value = self.adc.read()
        time.sleep_us(40)
        self.led.value(0)
        
        
        # Convert raw ADC value to voltage (assuming 3.3V reference)
        voltage = raw_value * (3.3 / 4095.0)

        # Convert voltage to dust density (calibration formula)
        dust_density = max((voltage - 0.4) / 0.05, 0)  # µg/m³
        return dust_density



def demo():
    gp2y1010_sensor = GP2Y1010(4, 36)
    dust_density = gp2y1010_sensor.read_dust_density()
    print(f"Dust Density: {dust_density:.2f} µg/m³")
    time.sleep(1)