import spidev
from gpiozero import DigitalOutputDevice
from time import sleep

scl_pin = 11  # SCLK
sda_pin = 10  # MOSI
res_pin = 19   # RES
dc_pin = 16    # DC
cs_pin = 10   # CS

spi_bus = 0
spi_device = 0

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000  # 1 MHz

res = DigitalOutputDevice(res_pin)
dc = DigitalOutputDevice(dc_pin)
cs = DigitalOutputDevice(cs_pin)

def oled_init():
    res.off()
    sleep(0.2)
    res.on()

    oled_wr_byte(0xAE, 0)  # turn off oled panel
    oled_wr_byte(0x00, 0)  # set low column address
    oled_wr_byte(0x10, 0)  # set high column address
    oled_wr_byte(0x40, 0)  # set start line address  Set Mapping RAM Display Start Line (0x00~0x3F)
    oled_wr_byte(0x81, 0)  # set contrast control register
    oled_wr_byte(0xCF, 0)  # Set SEG Output Current Brightness
    oled_wr_byte(0xA1, 0)  # Set SEG/Column Mapping     0xa0左右反置 0xa1正常
    oled_wr_byte(0xC8, 0)  # Set COM/Row Scan Direction   0xc0上下反置 0xc8正常
    oled_wr_byte(0xA6, 0)  # set normal display
    oled_wr_byte(0xA8, 0)  # set multiplex ratio(1 to 64)
    oled_wr_byte(0x3f, 0)  # 1/64 duty
    oled_wr_byte(0xD3, 0)  # set display offset Shift Mapping RAM Counter (0x00~0x3F)
    oled_wr_byte(0x00, 0)  # not offset
    oled_wr_byte(0xd5, 0)  # set display clock divide ratio/oscillator frequency
    oled_wr_byte(0x80, 0)  # set divide ratio, Set Clock as 100 Frames/Sec
    oled_wr_byte(0xD9, 0)  # set pre-charge period
    oled_wr_byte(0xF1, 0)  # Set Pre-Charge as 15 Clocks & Discharge as 1 Clock
    oled_wr_byte(0xDA, 0)  # set com pins hardware configuration
    oled_wr_byte(0x12, 0)
    oled_wr_byte(0xDB, 0)  # set vcomh
    oled_wr_byte(0x40, 0)  # Set VCOM Deselect Level
    oled_wr_byte(0x20, 0)  # Set Page Addressing Mode (0x00/0x01/0x02)
    oled_wr_byte(0x02, 0)
    oled_wr_byte(0x8D, 0)  # set Charge Pump enable/disable
    oled_wr_byte(0x14, 0)  # set(0x10) disable
    oled_clear()
    oled_wr_byte(0xAF, 0)  # display ON

def oled_color_turn(i):
    if not i:
        oled_wr_byte(0xA6, 0)  # normal display
    else:
        oled_wr_byte(0xA7, 0)  # inverse display

def oled_display_turn(i):
    if i == 0:
        oled_wr_byte(0xC8, 0)  # normal display
        oled_wr_byte(0xA1, 0)
    else:
        oled_wr_byte(0xC0, 0)  # reverse display
        oled_wr_byte(0xA0, 0)

def oled_wr_byte(dat, cmd):
    if cmd:
        dc.on()
    else:
        dc.off()

    cs.off()
    spi.xfer2([dat])
    cs.on()
    dc.on()

def oled_set_pos(x, y):
    oled_wr_byte(0xb0 + y, 1)  # 设置页地址（0~7）
    oled_wr_byte(((x & 0xf0) >> 4) | 0x10, 1)  # 设置显示

