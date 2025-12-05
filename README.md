# Indoor air quality monitoring system

## 1. Project Overview

### Problem Statement
Indoor air quality has a direct impact on comfort, health, and productivity. Many indoor environments (classrooms, apartments, offices) lack continuous, reliable, and accessible monitoring of key air-quality indicators such as temperature Humidity, CO₂ concentration or particulate matter (PM2.5 / PM10). Without real-time monitoring, it is difficult to detect poor ventilation conditions or pollution peaks.

### Proposed Solution
The goal of this project is to design a compact, MCU-based air-quality monitoring station. An ESP32 microcontroller serves as the system’s core, offering Wi-Fi connectivity and sufficient GPIO interfaces to read sensors and drive the display. The MCU communicates with the temperature/humidity sensor (I2C), as well as CO₂ and dust sensors, processes the data, and sends it to ThingSpeak via HTTP requests while updating the OLED screen with the latest readings. This results in a fully autonomous environmental monitoring device.

## 2.1 List of hardware components

| Component | Type | Primary Role / Function | Datasheet / Reference |
|----------|------|-------------------------|---------------------|
| **ESP32 (MicroPython pre-installed)** | Microcontroller board | Runs the main program, handles sensors and display |  |
| **SH1106 OLED Display (128×64)** | Display module | Shows sensor data and system information |  |
| **DHT12** | Temperature & humidity sensor | Measures ambient temperature and relative humidity |  |
| **MQ135 (FC-22)** | Gas / air quality sensor | Detects CO₂-equivalent and general air pollutants (analog output) | [MQ135 Arduino Library](https://hackaday.io/project/3475-sniffing-trinket/log/12363-mq135-arduino-library) |
| **GP2Y1010AU0F (Sharp)** | Optical dust sensor | Measures particulate matter concentration using IR scattering | [GP2Y1010AU0F (Sharp) Library][https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y1010au_appl_e.pdf) |
| **Breadboard** | Prototyping board | Allows assembling and connecting components without soldering |  |
| **Jumper Wires** | Wiring accessories | Used to connect sensors, display, and ESP32 on the breadboard |  |



## 2.2 Schematic

## 2.3 Pinout table

| Component                  | Component Pin / Signal | ESP32 Pin (GPIO) | Function / Role                        |
|----------------------------|----------------------|-----------------|----------------------------------------|
| DHT12 (Temperature/Humidity) | SDA                  | 21              | I2C data line for reading sensor values |
|                              | SCL                  | 22              | I2C clock line for sensor communication |
| OLED Display                | SDA                  | 21              | Shared I2C data line to display text    |
|                              | SCL                  | 22              | Shared I2C clock line for display       |
| MQ-135 (CO2 Proxy)          | A0 (Analog Out)      | 36              | Measures CO₂ equivalent via ADC         |
| GP2Y1010 (Particles)        | Vo (Analog Out)      | 39              | Reads particulate matter via ADC        |
|                              | LED Control          | 15              | Pulses IR LED to perform particle sensing |
| Power                       | VCC/VDD              | 3V3             | Provides 3.3V supply to sensors        |
| Ground                      | GND                  | GND             | Common ground for all components       |

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
