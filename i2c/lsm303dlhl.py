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
        strout = '(' + str(hex(self._data)) + ') '
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


class CraRegM(I2CRegisterConfiguration):
    __REGISTER_ADDRESS = 0x00

    __TEMPERATURE_ENABLE = 0x80

    DATA_OUTPUT_75 = 0x0
    DATA_OUTPUT_150 = 0x1
    DATA_OUTPUT_300 = 0x2
    DATA_OUTPUT_750 = 0x3
    DATA_OUTPUT_1500 = 0x4
    DATA_OUTPUT_3000 = 0x5
    DATA_OUTPUT_7500 = 0x6
    DATA_OUTPUT_22000 = 0x7

    def __init__(self, temperature=False, datarate=0x7):
        """

        :param temperature:
        :param datarate:
        """
        data = 0
        if temperature:
            data = 0x1
        data = data << 5
        data = data | (datarate & 0x7)
        data = data << 2
        super(CraRegM, self).__init__(self.__REGISTER_ADDRESS, data)

    def __str__(self):
        strout = '(' + str(hex(self._data)) + ') '
        if self._data & self.__TEMPERATURE_ENABLE:
            strout += 'Temperature enable '
        tmp = (self._data >> 2) & 0x7
        strout += ' output data rate: '
        if tmp == self.DATA_OUTPUT_75:
            strout += '0.75'
        if tmp == self.DATA_OUTPUT_150:
            strout += '1.5'
        if tmp == self.DATA_OUTPUT_300:
            strout += '3.0'
        if tmp == self.DATA_OUTPUT_750:
            strout += '7.5'
        if tmp == self.DATA_OUTPUT_1500:
            strout += '15'
        if tmp == self.DATA_OUTPUT_3000:
            strout += '30'
        if tmp == self.DATA_OUTPUT_7500:
            strout += '75'
        if tmp == self.DATA_OUTPUT_22000:
            strout += '220'
        strout += ' Hz'
        return strout


class CrbRegM(I2CRegisterConfiguration):
    __REGISTER_ADDRESS = 0x01

    RESOLUTION_13 = 0x20
    RESOLUTION_19 = 0x40
    RESOLUTION_25 = 0x60
    RESOLUTION_40 = 0x80
    RESOLUTION_47 = 0xa0
    RESOLUTION_56 = 0xc0
    RESOLUTION_81 = 0xe0

    def __init__(self, resolution=0xe0):
        super(CrbRegM, self).__init__(self.__REGISTER_ADDRESS, resolution)

    def __str__(self):
        strout = '(' + str(hex(self._data)) + ') Sensor input field range: (+/-)'
        if self._data == self.RESOLUTION_13:
            strout += '1.3'
        if self._data == self.RESOLUTION_19:
            strout += '1.9'
        if self._data == self.RESOLUTION_25:
            strout += '2.5'
        if self._data == self.RESOLUTION_40:
            strout += '4.0'
        if self._data == self.RESOLUTION_47:
            strout += '4.7'
        if self._data == self.RESOLUTION_56:
            strout += '5.6'
        strout += ' G'
        if self._data == self.RESOLUTION_81:
            strout += '8.1'
        return strout

class MrRegM(I2CRegisterConfiguration):
    __REGISTER_ADDRESS = 0x02

    CONTINUOUS_CONVERTION_MODE = 0x00
    SINGLE_CONVERTION_MODE = 0x01
    SLEEP_MODE = 0x02

    def __init__(self, mode=0x00):
        super(MrRegM, self).__init__(self.__REGISTER_ADDRESS, mode)

    def __str__(self):
        strout = '(' + hex(self._data) + ') '
        if self._data == self.CONTINUOUS_CONVERTION_MODE:
            strout += 'Continuous-conversion mode'
        if self._data == self.SINGLE_CONVERTION_MODE:
            strout += 'Single-conversion mode'
        if self._data in [self.SLEEP_MODE, 0x30]:
            strout += 'Sleep-mode. Device is placed in sleep-mode'
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
    MAG_ADDRESS = 0x1e

    __OUT_STATUS = 0x27

    __OUT_X_L_A = 0x28
    __OUT_X_H_A = 0x29
    __OUT_Y_L_A = 0x2a
    __OUT_Y_H_A = 0x2b
    __OUT_Z_L_A = 0x2c
    __OUT_Z_H_A = 0x2d

    __OUT_X_H_M = 0x3
    __OUT_X_L_M = 0x4
    __OUT_Y_H_M = 0x5
    __OUT_Y_L_M = 0x6
    __OUT_Z_H_M = 0x7
    __OUT_Z_L_M = 0x8

    __bus = None
    __ctrl_reg1_a = CtrlReg1A()
    __cra_reg_m = CraRegM()
    __crb_reg_m = CrbRegM()
    __mr_reg_m = MrRegM()

    def __init__(self, bus, ctrlReg1=None):
        self.__bus = bus
        if ctrlReg1 is not None:
            self.__ctrl_reg1_a = ctrlReg1
        bus.save_configuration(self.__ctrl_reg1_a, self.ACC_ADDRESS)
        bus.save_configuration(self.__cra_reg_m, self.MAG_ADDRESS)
        bus.save_configuration(self.__crb_reg_m, self.MAG_ADDRESS)
        bus.save_configuration(self.__mr_reg_m, self.MAG_ADDRESS)

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

    def get_magnetic_data(self):
        out = [0, 0, 0]
        self.__bus.start_comunication(self.MAG_ADDRESS)
        tmp_l = self.__bus.read_byte(self.__OUT_X_L_M)
        tmp_h = self.__bus.read_byte(self.__OUT_X_H_M)
        out[0] = c_int16(tmp_h << 8 | tmp_l).value
        tmp_l = self.__bus.read_byte(self.__OUT_Y_L_M)
        tmp_h = self.__bus.read_byte(self.__OUT_Y_H_M)
        out[1] = c_int16(tmp_h << 8 | tmp_l).value
        tmp_l = self.__bus.read_byte(self.__OUT_Z_L_M)
        tmp_h = self.__bus.read_byte(self.__OUT_Z_H_M)
        out[2] = c_int16(tmp_h << 8 | tmp_l).value
        self.__bus.stop_comunication()
        return out
