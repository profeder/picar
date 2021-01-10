from i2c.i2c_bus import I2CRegisterConfiguration
from ctypes import c_int16


class CtrlReg1A(I2CRegisterConfiguration):
    __POWER_OFF = 0x0
    __DATA_RATE_1 = 0x1
    __DATA_RATE_10 = 0x2
    __DATA_RATE_25 = 0x3
    __DATA_RATE_50 = 0x4
    __DATA_RATE_100 = 0x5
    __DATA_RATE_200 = 0x6
    __DATA_RATE_400 = 0x7
    __DATA_LOW_POWER_MODE_1620 = 0x8
    __DATA_1344_LP_5376 = 0x9

    LOW_POWER_MODE = 0x8

    Z_AXIS_ENABLE = 0x4
    Y_AXIS_ENABLE = 0x2
    X_AXIS_ENABLE = 0x1

    REGISTER_ADDRESS = 0x20

    def __init__(self, data_rate=0x2, axies_enables=0x7):
        data = data_rate << 4 | axies_enables
        super(CtrlReg1A, self).__init__(self.REGISTER_ADDRESS, data)

    def set_datarate(self, mode):
        super(self)._data = 0xf0 & (mode << 8)

    def set_low_power_mode_on(self):
        super(self)._data = (super(self)._data & 0xf7) | 0x08

    def set_low_power_mode_off(self):
        super(self)._data = super(self)._data & 0xf7

    def get_axis_number(self):
        axis = 0
        nibl = self._data & 0x07
        if nibl == 7:
            axis = 3
        if nibl in [6, 5, 3]:
            axis = 2
        if nibl in [1, 2, 4]:
            axis = 1
        return axis

    def power_on(self):
        return self.get_data() >> 4 != self.__POWER_OFF

    def x_enable(self):
        return self._data and self.X_AXIS_ENABLE

    def y_enable(self):
        return self._data and self.X_AXIS_ENABLE

    def z_enable(self):
        return self._data and self.X_AXIS_ENABLE

    def __str__(self):
        strout = str(hex(self._data)) + ' '
        nibh = (self._data >> 4) & 0x0f
        if nibh == self.__POWER_OFF:
            strout += 'Power off'
        else:
            nibl = self._data & 0x0f
            if nibl & self.LOW_POWER_MODE:
                strout += 'Low power mode '
            else:
                strout += 'Normal power mode '

            if nibh == self.__DATA_RATE_1:
                strout += 'datarate 1Hz: '
            if nibh == self.__DATA_RATE_10:
                strout += 'datarate 10Hz: '
            if nibh == self.__DATA_RATE_25:
                strout += 'datarate 25Hz: '
            if nibh == self.__DATA_RATE_50:
                strout += 'datarate 50Hz: '
            if nibh == self.__DATA_RATE_100:
                strout += 'datarate 100Hz: '
            if nibh == self.__DATA_RATE_200:
                strout += 'datarate 200Hz: '
            if nibh == self.__DATA_RATE_400:
                strout += 'datarate 400Hz: '
            strout += '['
            if nibl & self.X_AXIS_ENABLE:
                strout += 'x, '
            if nibl & self.Y_AXIS_ENABLE:
                strout += 'y, '
            if nibl & self.Z_AXIS_ENABLE:
                strout += 'z, '
            strout = strout[:-2] + ']'
        return strout


class LSM303DLHL:
    """
    The LSM303DLHC is a system-in-package featuring a 3D digital linear acceleration sensor and a 3D digital magnetic
    sensor.

    LSM303DLHC has linear acceleration full-scales of ±2g / ±4g / ±8g / ±16g and a magnetic field full-scale of
    ±1.3 / ±1.9 / ±2.5 / ±4.0 / ±4.7 / ±5.6 / ±8.1 gauss. All full-scales available are fully selectable by the user.

    LSM303DLHC includes an I2C serial bus interface that supports standard and fast mode 100 kHz and 400kHz.
    The system can be configured to generate interrupt signals by inertial wake-up/free-fall events as well as by the
    position of the device itself. Thresholds and timing of interrupt generators are programmable by the end user on
    the fly. Magnetic and accelerometer parts can be enabled or put into power-down mode separately.
    The LSM303DLHC is available in a plastic land grid array package (LGA) and is guaranteed to operate over an extended
    temperature range from -40 °C to +85 °C.
    """

    ACC_ADDRESS = 0x19

    __OUT_STATUS = 0x27

    __OUT_X_L_A = 0x28
    __OUT_X_H_A = 0x29

    __OUT_Y_L_A = 0x2a
    __OUT_Y_H_A = 0x2b

    __OUT_Z_L_A = 0x2c
    __OUT_Z_H_A = 0x2d

    __bus = None
    __ctrl_reg1_a = CtrlReg1A()

    def __init__(self, bus, ctrlReg1=None):
        self.__bus = bus
        if ctrlReg1 is not None:
            self.__ctrl_reg1_a = ctrlReg1
        bus.save_configuration(self.__ctrl_reg1_a, self.ACC_ADDRESS)

    def get_accelerometer_data(self):
        out = [0, 0, 0]
        if self.__ctrl_reg1_a.power_on():
            self.__bus.start_comunication(self.ACC_ADDRESS)
            status = self.__bus.read_byte(self.__OUT_STATUS)
            if status & 0x01 and self.__ctrl_reg1_a.x_enable():
                x_h = self.__bus.read_byte(self.__OUT_X_H_A)
                x_l = self.__bus.read_byte(self.__OUT_X_L_A)
                out[0] = c_int16(x_h << 8 | x_l).value
            if status & 0x02 and self.__ctrl_reg1_a.y_enable():
                y_h = self.__bus.read_byte(self.__OUT_Y_H_A)
                y_l = self.__bus.read_byte(self.__OUT_Y_L_A)
                out[1] = c_int16(y_h << 8 | y_l).value
            if status & 0x04 and self.__ctrl_reg1_a.z_enable():
                z_h = self.__bus.read_byte(self.__OUT_Z_H_A)
                z_l = self.__bus.read_byte(self.__OUT_Z_L_A)
                out[2] = c_int16(z_h << 8 | z_l).value
            self.__bus.stop_comunication()
        return out
