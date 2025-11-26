Problem Statement
Indoor air quality has a direct impact on comfort, health, and productivity. Many indoor environments (classrooms, apartments, offices) lack continuous, reliable, and accessible monitoring of key air-quality indicators such as:
•	Temperature
•	Humidity
•	CO₂ concentration
•	Particulate matter (PM2.5 / PM10)
Without real-time monitoring, it is difficult to detect poor ventilation conditions or pollution peaks.
Proposed Solution
The goal of this project is to design a compact MCU-based air-quality monitoring station capable of:
1.	Measuring multiple environmental parameters using several sensors.
2.	Collecting data periodically (e.g., every 5 minutes).
3.	Sending the data to ThingSpeak via Wi-Fi for cloud storage, visualization, and analysis.
4.	Displaying the measurements locally on an OLED screen in real time.
An ESP32 microcontroller is used as the core of the system. It integrates Wi-Fi capability and provides enough GPIO interfaces to read the sensors and drive the display. The MCU:
•	communicates with the temperature/humidity sensor (I2C)
•	reads the CO₂ sensor and dust sensor
•	processes the collected data
•	sends the data to ThingSpeak using HTTP requests
•	updates the OLED screen with the latest values
This creates a complete, autonomous environmental monitoring device.


#List of hardware components
Provide a list of sensors, actuators, and other electronic components intended for use.
Include justification for your component choices (why each part is needed).

ESP32 board with pre-installed MicroPython firmware, USB cable

SH1106 I2C OLED display 128x64 

DHT12 : temperature and humidity sensor, I2C (see lab)

MQ135 (with FC-22): CO2 detector, using library (to translate)
https://hackaday.io/project/3475-sniffing-trinket/log/12363-mq135-arduino-library

GP2Y1010AU0F (Sharp): Compact Optical Dust Sensor. It uses an optical sensing system (IRED diode and phototransistor) to measure light reflected by airborne dust. https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y1010au_e.pdf


#Software design
Present system-level block diagrams, flowcharts, or pseudocode showing the planned software logic and control flow.


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
