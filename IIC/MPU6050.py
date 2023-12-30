#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smbus			#import SMBus module of I2C
from time import sleep          #import

import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("./LCD")
from LCD.lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG) 

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


disp = LCD_1inch69.LCD_1inch69()

# Initialize library.
disp.Init()
    # Clear display.
disp.clear()
#Set the backlight to 100
disp.bl_DutyCycle(50)

logging.info("show image")
#ImagePath = ["../pic/Rspi.jpg"]
image = Image.open("./LCD/pic/Raspi.jpg")	
disp.ShowImage(image)
time.sleep(2)

Font1 = ImageFont.truetype("./LCD/Font/Font01.ttf", 25)
Font2 = ImageFont.truetype("./LCD/Font/Font01.ttf", 35)
Font3 = ImageFont.truetype("./LCD/Font/Font02.ttf", 32)

Ax = 0
Ay = 0
Az = 0
Gx = 0
Gy = 0

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

while True:

    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = round(acc_x/16384.0,5)
    Ay = round(acc_y/16384.0,5)
    Az = round(acc_z/16384.0,5)
    
    Gx = round(gyro_x/131.0,5)
    Gy = round(gyro_y/131.0,5)
    Gz = round(gyro_z/131.0,5)
    

    print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
    sleep(1)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)

#    logging.info("draw text")
    draw.text((60, 2), 'MPU6050', fill = "BLACK", font=Font3)
    draw.text((2, 30),'Ax=' , fill = "BLACK", font=Font3)
    draw.text((60, 30),str(Ax) , fill = "BLACK", font=Font3)
    draw.text((2, 70),'Ay=' , fill = "BLACK", font=Font3)
    draw.text((60, 70),str(Ay) , fill = "BLACK", font=Font3)
    draw.text((2, 110),'Az=' , fill = "BLACK", font=Font3)
    draw.text((60, 110),str(Az) , fill = "BLACK", font=Font3)
    draw.text((2, 150),'Gx=' , fill = "BLACK", font=Font3)
    draw.text((60, 150),str(Gx) , fill = "BLACK", font=Font3)
    draw.text((2, 190),'Gy=' , fill = "BLACK", font=Font3)
    draw.text((60, 190),str(Gy) , fill = "BLACK", font=Font3)
    draw.text((2, 230),'Gz=' , fill = "BLACK", font=Font3)
    draw.text((60, 230),str(Gz) , fill = "BLACK", font=Font3)

    image1=image1.rotate(0)
    disp.ShowImage(image1)
    time.sleep(1)

    # display with hardware SPI:
    #disp = LCD_1inch69.LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
