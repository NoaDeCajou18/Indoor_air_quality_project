import time

class GP2Y1010:
    """
    @class GP2Y1010
    @brief Minimal driver using external ADC and LED Pin objects.
           Returns voltage and PM2.5, no warnings or status LEDs.
    """

    ## @brief Constructor
    ## @param[in] adc_obj      ADC object connected to Vo output
    ## @param[in] led_pin_obj  Pin object to control IR LED
    def __init__(self, adc_obj, led_pin_obj):
        self.adc = adc_obj
        self.led = led_pin_obj
        self.led.value(0)  # Ensure LED is off at startup

    ## @brief Perform a single measurement of the sensor
    ## @return tuple (voltage, pm25)
    ##         voltage : analog output in volts
    ##         pm25    : estimated PM2.5 concentration in µg/m³
    def read(self):
        # Turn on IR LED for ~320 microseconds
        self.led.value(1)
        time.sleep_us(320)

        # Read ADC while LED is on
        raw = self.adc.read()

        # Turn off LED
        self.led.value(0)

        # Wait ~10 ms before next measurement
        time.sleep_ms(10)

        # Convert ADC value to voltage (ESP32 12-bit ADC, 0-3.3V)
        v = raw * (3.3 / 4095.0)

        # Estimate PM2.5 using standard linear approximation
        pm = max((voltage - 0.9) / 0.005, 0)

        return voltage, pm25

