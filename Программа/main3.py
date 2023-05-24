from VL53L0X import VL53L0X
from time import sleep_ms,sleep
from machine import Pin, Timer, I2C, WDT,SoftI2C


i2c_bus = SoftI2C(sda=Pin(16), scl=Pin(17),freq=400000)
tof = VL53L0X(i2c_bus)

while(1):
    tof.start()
    d=tof.read()
    tof.stop()
    print(d)
        
    
    
    