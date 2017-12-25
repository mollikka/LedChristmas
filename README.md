# LedChristmas
Turn the Christmas tree into a 3D led show

[Watch it in action](https://www.youtube.com/watch?v=jvAs8jxLCvw)

## Requirements

- Python3
- PIL/Pillow
- pyserial

- Arduino IDE
- FastLED

## Setup
A Christmas tree is decorated with an addressable RGB led strip.
To work, the Led Christmas needs 3D coordinates of each led.

The led strip is connected to a power supply and an Arduino unit.
Two network cameras are positioned to look at the Christmas tree at
a 90 degree angle of one another.

fastledcalib.ino is loaded on the Arduino.
This programs it to wait for a number on the serial connection.
When a number is given over the serial connection, the Arduino lights the
corresponding led.

The calibration script main.py commands Arduino to light each led
one at a time and displays two pictures from the cameras.
The user needs to click the position of the light in each camera.
To move to the next led, simply press enter.

When each led position has been read, the calibration script saves the data
with the command "save".
