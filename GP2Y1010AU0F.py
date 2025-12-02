import time

def read_gp2y1010(adc_obj, led_pin_obj):
    """
    @brief Perform a single measurement of GP2Y1010
    @param[in] adc_obj      ADC object connected to Vo output
    @param[in] led_pin_obj  Pin object to control IR LED
    @return tuple (voltage, pm25)
             voltage : analog output in volts
             pm25    : estimated PM2.5 concentration in µg/m³
    """

    # Turn on IR LED for ~320 µs
    led_pin_obj.value(1)
    time.sleep_us(320)

    # Read ADC while LED is on
    raw = adc_obj.read()

    # Turn off LED
    led_pin_obj.value(0)

    # Wait ~10 ms before next measurement
    time.sleep_ms(10)

    # Convert ADC value to voltage (ESP32 12-bit ADC, 0-3.3V)
    voltage = raw * (3.3 / 4095.0)

    # Estimate PM2.5 using standard linear approximation
    pm25 = max((voltage - 0.9) / 0.005, 0)

    return voltage, pm25

