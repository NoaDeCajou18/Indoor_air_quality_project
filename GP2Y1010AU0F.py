from machine import ADC, Pin, PWM
import time

# ---------------------------------------------------------------------------
# Sharp GP2Y1010AU0F Dust Sensor - MicroPython Class
# ---------------------------------------------------------------------------

class GP2Y1010:
    """
    MicroPython driver for the Sharp GP2Y1010AU0F dust sensor.
    Uses ADC to read dust concentration and PWM/Timer for LED control if needed.
    """

    def __init__(self, adc_pin=34, led_pwm_pin=None, led_freq=1000):
        """
        Initialize the GP2Y1010 sensor.
        
        :param adc_pin: GPIO pin connected to Vo (analog output)
        :param led_pwm_pin: GPIO pin to control LED via PWM (optional, can be None if LED powered directly)
        :param led_freq: PWM frequency in Hz
        """
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)  # 0–3.3V
        self.led_pwm = None
        if led_pwm_pin is not None:
            self.led_pwm = PWM(Pin(led_pwm_pin))
            self.led_pwm.freq(led_freq)
            self.led_pwm.duty(0)  # start off

    def pulse_led(self, duration_us=280):
        """
        Pulse the LED for a short duration. If using direct VCC supply, just wait duration.
        :param duration_us: microseconds to keep LED on before reading ADC
        """
        if self.led_pwm:
            self.led_pwm.duty(1023)  # max brightness
        time.sleep_us(duration_us)
        if self.led_pwm:
            self.led_pwm.duty(0)

    def read(self):
        """
        Read the dust sensor value.
        
        :return: (voltage, dust concentration µg/m3)
        """
        # Pulse the LED
        self.pulse_led()

        # Read ADC
        val = self.adc.read()

        # Wait 10 ms after LED pulse to respect timing
        time.sleep_ms(10)

        # Convert ADC to voltage
        voltage = val * 3.3 / 4095.0

        # Convert voltage to dust concentration (µg/m³)
        dust = max((voltage - 0.9) * 200.0, 0.0)

        return voltage, dust

# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Si LED branchée directement sur VCC, mettre led_pwm_pin=None
    sensor = GP2Y1010(adc_pin=34, led_pwm_pin=None)
    
    while True:
        voltage, dust = sensor.read()
        print("Voltage:", voltage, "V   Dust:", dust, "µg/m³")
        time.sleep(1)

