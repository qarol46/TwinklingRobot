from machine import Pin,I2C
from TCS34725 import *
from time import sleep_ms,sleep
import uasyncio as asio

i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)
tcs.gain(4)#gain must be 1, 4, 16 or 60
tcs.integration_time(80)
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta']
col_id = 0

while 1:
    #await asio.sleep_ms(int_ms)
    r,g,b=tcs.read(1)[0],tcs.read(1)[1],tcs.read(1)[2]
    h,s,v=rgb_to_hsv(r,g,b)
    if 0<h<60:
        col_id=0
    elif 61<h<120:
        col_id=1
    elif 70<h<180:
        if s<30 and v>5:
            col_id=2
        else:
            col_id=3
    if h<5 and s<5 and v<4:
        col_id=4
    elif 181<h<250:
        if s>20:
            col_id=5
        else:
            col_id=6
    elif 241<h<360:
        col_id=7 
    print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))
            
