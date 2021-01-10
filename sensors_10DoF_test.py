from i2c.bmp180 import BMP180
from i2c.i2c_bus import I2CBus
from i2c.lsm303dlhl import *
from time import sleep
from util.utils import get_compass

bus = I2CBus(1)
# conf = CtrlReg1A(0x01, CtrlReg1A.X_AXIS_ENABLE|CtrlReg1A.Z_AXIS_ENABLE)
acc = LSM303DLHL(bus)
bar = BMP180(bus)
bar.set_mode(BMP180.ULTRA_LOW_POWER_MODE)
while True:
    print('Acc: ' + repr(acc.get_accelerometer_data()))
    mag = acc.get_magnetic_data()
    print('Mag: ' + repr(mag))
    print('Compass: ' + str(get_compass(mag)))
    t, p = bar.get_data()
    print('Temp: ' + str(t) + '°C')
    print('Pres: ' + str(p) + ' Pa')
    sleep(5)
