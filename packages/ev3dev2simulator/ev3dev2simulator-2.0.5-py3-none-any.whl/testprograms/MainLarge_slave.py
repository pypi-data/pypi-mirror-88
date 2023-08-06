#!/usr/bin/env python3

from ev3dev2._platform.ev3 import INPUT_1, INPUT_4, INPUT_2, INPUT_3, OUTPUT_B
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import TouchSensor
from testprograms.BluetoothHelper import BluetoothHelper

bth = BluetoothHelper()
bth.connect_as_client()

leds = Leds()
leds.animate_rainbow()
ts1 = TouchSensor(INPUT_2)
ts2 = TouchSensor(INPUT_3)

while True:
    leds.animate_rainbow()
