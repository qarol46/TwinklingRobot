from VL53L0X import *
from time import sleep_ms,sleep
from machine import Pin, Timer, I2C, WDT,SoftI2C


i2c_bus = SoftI2C(sda=Pin(21), scl=Pin(22))
tof = VL53L0X(i2c_bus)

while(1):
    tof.start()
    d=tof.read()-65
    tof.stop()
    print(d)
        
    
    
    
    