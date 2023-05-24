from time import sleep_ms
from machine import Pin,Timer

R_m_pin = Pin(34, Pin.IN)
L_m_pin = Pin(21, Pin.IN)

def L_W_int(pin):
    global L_W_count
    L_W_count+=1

def R_W_int(pin):
    global R_W_count
    R_W_count+=1
    
L_m_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=L_W_int)
R_m_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=R_W_int)

L_W_count,R_W_count=0,0 
while(1):
    print(L_W_count)
    sleep_ms(200)