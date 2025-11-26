from machine import Pin, I2C
from sh1106 import SH1106_I2C


# -----------------------------------------------------------------------------
## @brief Initialize the OLED SH1106 display using I2C.
##
## This function configures the I2C bus (pins 22 and 21 on the ESP32),
## creates a global display object, clears the screen and prints a boot message.
##
## @return The initialized SH1106_I2C display object.
# -----------------------------------------------------------------------------
def init_oled():
    global oled

    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

    oled = SH1106_I2C(i2c)
    oled.sleep(False)
    oled.contrast(120)
    oled.fill(0)

    oled.text("Air Monitor", 20, 0)
    oled.text("OLED Ready", 25, 15)
    oled.show()

    return oled


# -----------------------------------------------------------------------------
## @brief Display current sensor values on the OLED screen.
##
## This function clears the OLED screen and writes:
##   - Temperature (°C)
##   - Humidity (%)
##   - CO2 concentration (ppm)
##   - Dust concentration (µg/m3)
##
## @param temp Temperature in °C (float)
## @param hum Humidity in % (float)
## @param co2 CO2 concentration in ppm (float)
## @param pm Dust concentration (PM2.5) in µg/m³ (float)
##
## @return None
# -----------------------------------------------------------------------------
def update_oled(temp, hum, co2, pm):
    global oled

    oled.fill(0)   # clear screen

    oled.text("Env Monitor", 15, 0)
    oled.text("T:  {:.1f} C".format(temp), 0, 15)
    oled.text("H:  {:.1f} %".format(hum), 0, 28)
    oled.text("CO2:{:.0f} ppm".format(co2), 0, 41)
    oled.text("PM: {:.1f} ug/m3".format(pm), 0, 53)

    oled.show()
