# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :   
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import sys
import time
import spidev
import logging
import numpy as np
from gpiozero import *

class RaspberryPi:
    def __init__(self,spi=spidev.SpiDev(0,0),rst =19,dc = 16,i2c=None,i2c_freq=100000):
        self.np=np
        self.INPUT = False
        self.OUTPUT = True

#        self._speed  = 40000000
#        self.BL_freq=bl_freq

        self._rst = self.gpio_mode(rst,self.OUTPUT)
        self._dc = self.gpio_mode(dc,self.OUTPUT)
#        self.BL_PIN = self.gpio_pwm(bl)
#        self.bl_DutyCycle(0)
        
        #Initialize SPI
        self._spi = spi
        if self._spi!=None :
#            self._spi.max_speed_hz = 40000000
            self._spi.mode = 0b00

    def gpio_mode(self,Pin,Mode,pull_up = None,active_state = True):
        if Mode:
            return DigitalOutputDevice(Pin,active_high = True,initial_value =False)
        else:
            return DigitalInputDevice(Pin,pull_up=pull_up,active_state=active_state)

    def digital_write(self, Pin, value):
        Pin = LED(Pin)
        if value:
            Pin.on()
        else:
            Pin.off()

    def digital_read(self, Pin):
        return Pin.value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

#    def gpio_pwm(self,Pin):
#        return PWMOutputDevice(Pin,frequency = self.BL_freq)

    def spi_writebyte(self, data):
        if self._spi!=None :
            self._spi.writebytes(data)

#    def bl_DutyCycle(self, duty):
#        self.BL_PIN.value = duty / 100
#        
#    def bl_Frequency(self,freq):# Hz
#        self.BL_PIN.frequency = freq
#           
    def module_init(self):
        if self._spi!=None :
#            self._spi.max_speed_hz = self._speed        
            self._spi.mode = 0b00     
        return 0

    def module_exit(self):
        logging.debug("spi end")
        if self._spi!=None :
            self._spi.close()
        
        logging.debug("gpio cleanup...")
        self.digital_write(self._rst, 1)
        self.digital_write(self._dc, 0)   
 #       self.BL_PIN.close()
        time.sleep(0.001)



'''
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
'''

### END OF FILE ###
