from machine import Pin,I2C
from neopixel import NeoPixel
from TCS34725 import *
from time import sleep_ms,sleep
import uasyncio as asio

i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)
tcs.gain(16)#gain must be 1, 4, 16 or 60
tcs.integration_time(120)
NUM_OF_LED = 3
np = NeoPixel(Pin(25), NUM_OF_LED)
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta']

col_id = 0
Lt = 255
direct = 0
debug = 1

async def color_det(int_ms):
    global color,col_id,debug
    while 1:
        await asio.sleep_ms(int_ms)
        r,g,b=tcs.read(1)[0],tcs.read(1)[1],tcs.read(1)[2]
        h,s,v=rgb_to_hsv(r,g,b)
        if 0<h<50:
            col_id=0
        elif 50<h<70:
            col_id=1
        elif 70<h<180:
            if v>5:
                col_id=2
            else:
                col_id=3
        if s<10 and v<4:
                col_id=4
        elif 181<h<250:
            if s>30:
                col_id=5
            else:
                col_id=6
        elif 241<h<360:
            col_id=7 
        if debug:
            print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))

async def LED_cont(int_ms):
    while 1:
        await asio.sleep_ms(int_ms)
        if col_id==0:
            np[0]=(Lt,0,0)
        elif col_id==1:
            np[0]=(Lt,Lt,0)
        elif col_id==2:
            np[0]=(Lt,Lt,Lt)
        elif col_id==3:
            np[0]=(0,Lt,0)
        elif col_id==4:
            np[0]=(0,0,0)
            np.write()
            await asio.sleep_ms(300)
            np[0]=(Lt,0,0)
        elif col_id==5:
            np[0]=(0,Lt,Lt)
        elif col_id==6:
            np[0]=(0,0,Lt) 
        elif col_id==7:
            np[0]=(Lt,0,Lt)
        np.write()

loop = asio.get_event_loop()
loop.create_task(color_det(0))
loop.create_task(LED_cont(0))
loop.run_forever()