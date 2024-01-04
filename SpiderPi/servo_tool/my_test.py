#!/usr/bin/env python3
import os
import sys
import time
from gpiozero import DigitalOutputDevice
from BusServoCmd import *
from smbus2 import SMBus, i2c_msg
from BusServoControl import *


id = getBusServoID() 
print("ServoID:",id)
