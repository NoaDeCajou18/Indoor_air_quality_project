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


DHT12 : temperature and humidity sensor, I2C (see lab)

SDS011 : Laser dust sensor. Detect particles with a diameter >03μm, designed to measure PM2.5 and PM10
https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y1010au_e.pdf

MQ135 (with FC-22): CO2 detector, using library (to translate)
https://hackaday.io/project/3475-sniffing-trinket/log/12363-mq135-arduino-library

GP2Y1010AU0F (Sharp): Compact Optical Dust Sensor. It uses an optical sensing system (IRED diode and phototransistor) to measure light reflected by airborne dust. It's particularly effective at detecting very fine particles like cigarette smoke. https://global.sharp/products/device/lineup/data/pdf/datasheet/gp2y1010au_e.pdf


#Software design
Present system-level block diagrams, flowcharts, or pseudocode showing the planned software logic and control flow.


```
init() //sensors, OLED, wifi connection, timer

timer_handle() :
 cnt +=1
 if cnt%PERIODE == 1:
  take_measure = True

while True:
 if take_measure :
  data = get_data()
  send_data(data, URL)
  OLED.print_data(data)
  take_measure = False
```
