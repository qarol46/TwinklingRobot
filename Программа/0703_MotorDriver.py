from MX1508 import *
from time import sleep_ms
from machine import Pin,Timer,MX1508,I2C

m1 = MX1508 (12, 13)
m2 = MX1508 (25, 26)
m3 = MX1508 (32, 33) #покдлючение моторов 

m1_pin = Pin(34, Pin.IN)
m2_pin = Pin(35, Pin.IN)
m3_pin = Pin(27, Pin.IN) # оптический инкодер

def m1_int(pin):
    global m1_count
    m1_count+=1
    
def m2_int(pin):
    global m1_count
    m2_count+=1
    
def m3_int(pin):
    global m1_count
    m3_count+=1


m1_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=m1_int)
m2_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=m2_int)
m3_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=m3_int)

timer = Timer(0)

def forward ( speed, dist, orient):
    global m1_count, m2_count,m3_count,direct
    
    while dist>=k*m1_count*math.pi*r 
    
    if orient==1:
        if m1_count>m2_count:
            m1.forward(0)
            m2.forward(Sp)
        elif m1_count<m2_count:
            m1.forward(Sp)
            m2.forward(0)
        else:
            m1.forward(Sp)
            m2.forward(Sp)
            
    if orient==2:
        if m1_count>m3_count:
            m1.forward(0)
            m3.forward(Sp)
        elif m1_count<m3_count:
            m1.forward(Sp)
            m3.forward(0)
        else:
            m1.forward(Sp)
            m3.forward(Sp)
            
    if orient==3:
        if m2_count>m3_count:
            m2.forward(0)
            m3.forward(Sp)
        elif m2_count<m3_count:
            m2.forward(Sp)
            m3.forward(0)
        else:
            m2.forward(Sp)
            m3.forward(Sp)
        
        m1.forward =(0)
        m2.forward =(0)
        m3.forward =(0) #конец цикла