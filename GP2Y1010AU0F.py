from machine import Pin, ADC
import time

# ---------------------------------------------------------------------------
#  Sharp GP2Y1010AU0F Dust Sensor - MicroPython Driver
# ---------------------------------------------------------------------------

## @brief Initialize hardware pins and ADC for the GP2Y1010 sensor.
## LED_PIN must be wired to the LED control pin of the sensor.
## ADC_PIN must be wired to the analog output pin (Vo) of the sensor.
led = Pin(25, Pin.OUT)        # LED control pin (adjust if needed)
adc = ADC(Pin(34))            # ADC input pin
adc.atten(ADC.ATTN_11DB)      # ADC range 0–3.3V

# ---------------------------------------------------------------------------
## @brief Read dust concentration from the GP2Y1010 sensor.
##
## The LED is pulsed ON for 280 microseconds, then the analog output
## is sampled. After that, the LED is turned OFF and we wait 10 ms
## to respect the sensor timing diagram.
##
## @return (voltage, dust)  
##         voltage in Volts (float)  
##         dust concentration in µg/m³ (float)
# ---------------------------------------------------------------------------
def read_gp2y1010():
    # Turn on IR LED
    led.value(1)

    # Wait the recommended 280 µs before reading ADC (Sharp datasheet)
    time.sleep_us(280)

    # Read raw ADC value (0-4095 on ESP32)
    val = adc.read()

    # Turn LED OFF
    led.value(0)

    # Wait 10 ms before next reading (required by sensor timing)
    time.sleep_ms(10)

    # Convert ADC to voltage
    voltage = val * 3.3 / 4095.0

    # Convert voltage to dust concentration (Sharp empirical formula)
    # Output = max(0, (Vo - 0.9) * 200)
    dust = max((voltage - 0.9) * 200.0, 0.0)

    return voltage, dust


# ---------------------------------------------------------------------------
#  Example usage (comment out in final integration)
# ---------------------------------------------------------------------------
## @brief Simple test loop printing sensor readings every second.
if __name__ == "__main__":
    while True:
        voltage, dust = read_gp2y1010()
        print("Voltage:", voltage, "V   Dust:", dust, "µg/m³")
        time.sleep(1)
