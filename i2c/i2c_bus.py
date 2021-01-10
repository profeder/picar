import threading
from ctypes import c_int16

from smbus import SMBus
from threading import Condition
from i2c.i2c_register_configuration import I2CRegisterConfiguration


class I2CRegisterConfiguration:
    _address = None
    _data = None

    def __init__(self):
        pass

    def __init__(self, address):
        self._address = address

    def __init__(self, address, data):
        self._address = address
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def __str__(self) -> str:
        pass

    def get_address(self):
        return self._address


class I2CBus:
    __cond = Condition()
    __busy = False
    __address = None
    __bus = None
    __thread_owner = None

    def __init__(self, bus):
        self.__bus = SMBus(bus)

    def __have_connection(self):
        return self.__thread_owner == threading.current_thread()

    def start_comunication(self, address):
        self.__cond.acquire()
        if self.__thread_owner is not None:
            self.__cond.wait()
        self.__thread_owner = threading.current_thread()
        self.__address = address

    def stop_comunication(self):
        self.__address = None
        self.__thread_owner = None
        self.__cond.notify()
        self.__cond.release()

    def read_byte(self, address):
        if not self.__have_connection():
            self.start_comunication(self.__address)
        data = self.__bus.read_byte_data(self.__address, address)
        return data

    def read_word(self, base_address, flip=False):
        if not self.__have_connection():
            self.start_comunication(self.__address)
        h = self.read_byte(base_address)
        l = self.read_byte(base_address + 1)
        data = h << 8 | l
        if flip:
            data = l << 8 | h
        return data

    def write_byte(self, address, data):
        if not self.__have_connection():
            self.start_comunication(self.__address)
        self.__bus.write_byte_data(self.__address, address, data)

    def get_configuration(self, conf, address=None):
        if not isinstance(conf, I2CRegisterConfiguration):
            raise Exception('Formato parametro conf non valido ' + str(type(conf)) + ' atteso '
                            + str(type(I2CRegisterConfiguration)))
        if address is None:
            address = self.__address
        self.start_comunication(address)
        data = self.read_byte(conf.get_address())
        conf.set_data(data)
        self.stop_comunication()
        return conf

    def save_configuration(self, conf, address=None):
        if not isinstance(conf, I2CRegisterConfiguration):
            raise Exception('Formato parametro conf non valido ' + str(type(conf)) + ' atteso '
                            + str(type(I2CRegisterConfiguration)))
        if address is None:
            address = self.__address
        self.start_comunication(address)
        self.write_byte(conf.get_address(), conf.get_data())
        self.stop_comunication()
