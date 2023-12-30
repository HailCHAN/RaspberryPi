#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level = logging.DEBUG)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch69.LCD_1inch69(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch69.LCD_1inch69()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)

    Font1 = ImageFont.truetype("../Font/Font01.ttf", 25)
    Font2 = ImageFont.truetype("../Font/Font01.ttf", 35)
    Font3 = ImageFont.truetype("../Font/Font02.ttf", 32)

    logging.info("show image")
    #ImagePath = ["../pic/Rspi.jpg"]
    image = Image.open("../pic/Raspi.jpg")	
    disp.ShowImage(image)
    time.sleep(2)

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)

    logging.info("draw text")
    draw.text((60, 2), 'MPU6050', fill = "BLACK", font=Font1)
    image1=image1.rotate(0)
    disp.ShowImage(image1)
    time.sleep(2)
    
#    image2 = Image.new("RGB", (disp.height,disp.width ), "WHITE")
#    draw = ImageDraw.Draw(image2)
#    draw.text((60, 2), u"    MPU6050", fill = 808000, font=Font3)
#    draw.text((100, 42), u"元  唐珙", fill = 808080, font=Font3)
#    draw.text((60, 82), u"西风吹老洞庭波，", fill = "BLUE", font=Font3)
#    draw.text((60, 122), u"一夜湘君白发多。", fill = "RED", font=Font3)
#    draw.text((60, 162), u"醉后不知天在水，", fill = "GREEN", font=Font3)
#    draw.text((60, 202), u"满船清梦压星河。", fill = "BLACK", font=Font3)
#    image2=image2.rotate(0)
#    disp.ShowImage(image2)
#    time.sleep(2)   

    disp.module_exit()
    logging.info("quit:")
    
   
except IOError as e:
    logging.info(e)    
    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
