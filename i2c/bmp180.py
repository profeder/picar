# sensore Barometrico/temperatura
from builtins import float, repr, pow, int
from ctypes import c_short
from ctypes import c_ushort
from ctypes import c_long
from ctypes import c_ulong
from time import sleep


class BMP180:
    """
    The BMP180 is the function compatible successor of the BMP085, a new generation of high precision digital pressure
    sensors for consumer applications.

    The ultra-low power, low voltage electronics of the BMP180 is optimized for use in mobile phones, PDAs,
    GPS navigation devices and outdoor equipment. With a low altitude noise of merely 0.25m at fast conversion time,
    the BMP180 offers superior performance. The I2C interface allows for easy system integration with a microcontroller.

    The BMP180 is based on piezo-resistive technology for EMC robustness, high accuracy and linearity as well as long
    term stability.

    """
    __oss = {'mode': 0, 'time': 0.045}

    DEVICE_ADDRESS = 0x77

    __bus = None

    __AC1 = c_short(408)
    __AC2 = c_short(-72)
    __AC3 = c_short(-14383)
    __AC4 = c_ushort(32741)
    __AC5 = c_ushort(32757)
    __AC6 = c_ushort(23153)
    __B1 = c_short(6190)
    __B2 = c_short(4)
    __B3 = 0
    __B4 = 0
    __B5 = 0
    __B6 = 0
    __B7 = 0
    __MB = c_short(-32768)
    __MC = c_short(-8711)
    __MD = c_short(2868)
    __test = False

    # Modalita' di campionamento
    ULTRA_LOW_POWER_MODE = {'mode': 0, 'time': 0.045}
    STANDARD = {'mode': 1, 'time': 0.075}
    HIGH_RESOLUTION = {'mode': 2, 'time': 0.135}
    ULTRA_HIGH_RESOLUTION = {'mode': 3, 'time': 0.255}

    def __init__(self, bus, test_mode=False):
        """

        :param bus: I2CBus
        :param test_mode: default false
        """
        self.__bus = bus
        self.__test = test_mode
        if not self.__test:
            self.__bus.start_comunication(self.DEVICE_ADDRESS)
            self.__AC1 = c_short(self.__bus.read_word(0xAA)).value
            self.__AC2 = c_short(self.__bus.read_word(0xAC)).value
            self.__AC3 = c_short(self.__bus.read_word(0xAE)).value
            self.__AC4 = c_ushort(self.__bus.read_word(0xB0)).value
            self.__AC5 = c_ushort(self.__bus.read_word(0xB2)).value
            self.__AC6 = c_ushort(self.__bus.read_word(0xB4)).value
            self.__B1 = c_short(self.__bus.read_word(0xB6)).value
            self.__B2 = c_short(self.__bus.read_word(0xB8)).value
            self.__MB = c_short(self.__bus.read_word(0xBA)).value
            self.__MC = c_short(self.__bus.read_word(0xBC)).value
            self.__MD = c_short(self.__bus.read_word(0xBE)).value
            self.__bus.stop_comunication()

    def set_mode(self, mode):
        self.__oss = mode

    def __read_temperature(self):
        ut = c_long(27898)
        if not self.__test:
            self.__bus.start_comunication(self.DEVICE_ADDRESS)
            self.__bus.write_byte(0xF4, 0x2E)
            sleep(0.45)
            ut = c_long(self.__bus.read_word(0xF6)).value
            self.__bus.stop_comunication()
        x1 = (ut - self.__AC6) * self.__AC5 / pow(2, 15)
        x2 = self.__MC * pow(2, 11) / (x1 + self.__MD)
        self.__B5 = x1 + x2
        t = (self.__B5 + 8) / pow(2, 4)
        return float(t) / 10

    def __read_pression(self):
        up = c_long(23843).value
        if not self.__test:
            self.__bus.start_comunication(self.DEVICE_ADDRESS)
            data = 0x34 + (self.__oss['mode'] << 6)
            self.__bus.write_byte(0xF4, data)
            sleep(self.__oss['time'])
            __MBs = self.__bus.read_byte(0xf6)
            lsb = self.__bus.read_byte(0xf7)
            xlsb = self.__bus.read_byte(0xf8)
            self.__bus.stop_comunication()
            up = c_long((__MBs << 16) + (lsb << 8) + xlsb >> (8 - self.__oss['mode'])).value

        self.__B6 = self.__B5 - 4000

        x1 = (self.__B2 * pow(self.__B6, 2) / pow(2, 12)) / pow(2, 11)
        x2 = self.__AC2 * self.__B6 / pow(2, 11)
        x3 = x1 + x2

        self.__B3 = ((int(self.__AC1 * 4 + x3) << self.__oss['mode']) + 2) / 4

        x1 = self.__AC3 * self.__B6 / pow(2, 13)
        x2 = (self.__B1 * pow(self.__B6, 2) / pow(2, 12)) / pow(2, 16)
        x3 = (x1 + x2 + 2) / 4

        self.__B4 = self.__AC4 * c_ulong(int(x3) + 32768).value / pow(2, 15)
        self.__B7 = c_ulong(up - int(self.__B3)).value * (50000 >> self.__oss['mode'])

        if self.__B7 < 0x80000000:
            p = (self.__B7 * 2) / self.__B4
        else:
            p = (self.__B7 / self.__B4) * 2

        x1 = pow(p / pow(2, 8), 2)
        x1 = (x1 * 3038) / pow(2, 16)
        x2 = (-7357 * p) / pow(2, 16)

        p = p + (x1 + x2 + 3791) / pow(2, 4)
        return int(p)

    def get_data(self):
        t = self.__read_temperature()
        p = self.__read_pression()
        return [t, p]

    def get_calibration(self):
        print('__AC1: ' + repr(self.__AC1))
        print('__AC2: ' + repr(self.__AC2))
        print('__AC3: ' + repr(self.__AC3))
        print('__AC4: ' + repr(self.__AC4))
        print('__AC5: ' + repr(self.__AC5))
        print('__AC6: ' + repr(self.__AC6))

        print('__B1: ' + repr(self.__B1))
        print('__B2: ' + repr(self.__B2))

        print('__MB: ' + repr(self.__MB))
        print('__MC: ' + repr(self.__MC))
        print('__MD: ' + repr(self.__MD))
