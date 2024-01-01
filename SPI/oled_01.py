import spidev
from gpiozero import DigitalOutputDevice
from time import sleep

class OLED:
    def __init__(self, spi_bus=0, spi_device=0, dc_pin=16, rst_pin=19):
        # 初始化 SPI
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 40000000  # 1 MHz

        # 初始化 GPIO 输出设备
        self.dc = DigitalOutputDevice(dc_pin)
        self.rst = DigitalOutputDevice(rst_pin)

        sleep(0.1)
        # 初始化 OLED
        self._command(0xAE)  # Display off
        self._command(0xD5, 0x80)  # Set display clock divide ratio/oscillator frequency
        self._command(0xA8, 0x3F)  # Set multiplex ratio (1 to 64)
        self._command(0xD3, 0x00)  # Set display offset
        self._command(0x40)  # Set start line address
        self._command(0x8D, 0x14)  # Charge pump setting (0x10: Enable, 0x14: Enable + boost)
        self._command(0x20, 0x00)  # Set memory addressing mode to horizontal
        self._command(0xA1)  # Set segment re-map
        self._command(0xC8)  # Set COM output scan direction
        self._command(0xDA, 0x12)  # Set COM pins hardware configuration
        self._command(0x81, 0xCF)  # Set contrast control
        self._command(0xD9, 0xF1)  # Set pre-charge period
        self._command(0xDB, 0x40)  # Set VCOMH deselect level
        self._command(0xA4)  # Entire display on (resume) / (output follows RAM content)
        self._command(0xA6)  # Set normal display (0xA7: inverted display)
        self._command(0x2E)  # Deactivate scroll
        self._command(0xAF)  # Display on
        self.spi.mode = 1  # 设置 SPI 模式为 0
        sleep(0.1)

    def _command(self, *args):
        # 发送命令
        self.dc.off()
        print("Sending command:",args)
        self.spi.xfer2(list(args))

    def _data(self, data):
        # 发送数据
        self.dc.on()
        print("Sending data:",data)
        self.spi.xfer2([data])

    def clear(self):
        # 清空屏幕
        self._command(0x20, 0x00)  # Set memory addressing mode to horizontal
        for i in range(8):
            self._command(0xB0 + i)  # Set page address
            self._command(0x00)  # Set lower column address
            self._command(0x10)  # Set higher column address
            for j in range(128):
                self._data(0x00)

    def show_text(self, text):
        # 在屏幕上显示文本
        self.clear()
        self._command(0x20, 0x00)  # Set memory addressing mode to horizontal
        for i, char in enumerate(text):
            self._data(ord(char))
        self._command(0xAF)  # Display on

    def cleanup(self):
        # 清理 GPIO 和 SPI
        self.spi.close()
        self.dc.close()
        self.rst.close()

if __name__ == "__main__":
    try:
        oled = OLED()
        oled.show_text("Hello, OLED!")
        sleep(5)  # 显示5秒钟
    finally:
        oled.cleanup()
