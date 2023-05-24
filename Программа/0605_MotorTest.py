from MX1508 import *
from time import sleep_ms
from machine import Pin,Timer

m2 = MX1508 (26, 27)
m1 = MX1508 (2, 4)
flag = 0
while(1):
    while flag == 0:
        m1.reverse(4096)
        m2.reverse(4096)
        sleep_ms(5000)
        flag = 1
    m1.forward(0)
    m2.forward(0)
    sleep_ms(200)
    m1.forward(4096)
    m2.reverse(4096)
    sleep_ms(1000)