# Indoor air quality monitoring system

## 1. Project Overview

### Problem Statement
Indoor air quality has a direct impact on comfort, health, and productivity. Many indoor environments (classrooms, apartments, offices) lack continuous, reliable, and accessible monitoring of key air-quality indicators such as temperature Humidity, CO₂ concentration or particulate matter (PM2.5 / PM10). Without real-time monitoring, it is difficult to detect poor ventilation conditions or pollution peaks.

### Proposed Solution
The goal of this project is to design a compact MCU-based air-quality monitoring station. An ESP32 microcontroller is used as the core of the system. It integrates Wi-Fi capability and provides enough GPIO interfaces to read the sensors and drive the display. The MCU communicates with the temperature/humidity (I2C), CO₂ and dust sensor then processes and sends them to ThingSpeak using HTTP requests and updates the OLED screen with the latest values. This creates a complete, autonomous environmental monitoring device.


## 2. List of hardware components

ESP32 board with pre-installed MicroPython firmware, USB cable

SH1106 I2C OLED display 128x64 

DHT12 : temperature and humidity sensor, I2C (see lab)

MQ135 (with FC-22): CO2 detector, using library (to translate)
https://hackaday.io/project/3475-sniffing-trinket/log/12363-mq135-arduino-library

GP2Y1010AU0F (Sharp): Compact Optical Dust Sensor. It uses an optical sensing system (IRED diode and phototransistor) to measure light reflected by airborne dust. https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y1010au_e.pdf
## 2. List of hardware components

| Component | Type | Primary Role / Function |
|----------|------|-------------------------|
| **ESP32 (MicroPython pre-installed)** | Microcontroller board | Runs the main program, handles sensors and display |
| **SH1106 OLED Display (128×64)** | Display module | Shows sensor data and system information |
| **DHT12** | Temperature & humidity sensor | Measures ambient temperature and relative humidity |
| **MQ135 (FC-22)** | Gas / air quality sensor | Detects CO₂-equivalent and general air pollutants (analog output) |
| **GP2Y1010AU0F (Sharp)** | Optical dust sensor | Measures particulate matter concentration using IR scattering |


## 3. Software design

```
init() //sensors, OLED, wifi connection, timer

timer : send event "take_measure" every PERIODE

while True:
 when "take_measure" received
  get data from DHT12 (temperature and humidity)
  get data from MQ135 (CO2)
  get data from SDS011 (particulate matter)
  send data to the api.thingspeak.com
  print data on OLED display
```
