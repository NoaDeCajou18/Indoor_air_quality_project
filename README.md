# Indoor_air_quality_project
Digital electronics 2 (DE2) class project


#Problem statement and solution overview
Clearly describe the problem being addressed.
Explain how your proposed solution uses MCU to solve it.


We want to measure temperature, humidity, CO2, and particulate matter (PM2.5/PM10).
 - collect data every 5 minutes (or other)
 - send it to api.thingspeak.com
 - display it on a OLED display

A MCU to collect data from sensors and send it by wifi and control OLED display to display it.


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
