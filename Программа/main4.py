from machine import Pin,I2C
from neopixel import NeoPixel
from MX1508 import *
from VL53L0X import *
from TCS34725 import *
from time import sleep_ms,sleep
import uasyncio as asio
 
i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)
tcs.gain(16) #gain must be 1, 4, 16 or 60 #уровень усиления цветодатчика
tcs.integration_time(120)
i2c_bus1 = I2C(1, sda=Pin(21), scl=Pin(22)) #tof - time of flight
tof = VL53L0X(i2c_bus1)
NUM_OF_LED = 3 #количество светодиодов
np = NeoPixel(Pin(25), NUM_OF_LED) #подключение светодиода
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta'] #список из определяемых цветов
motor_L = MX1508(4, 2)
motor_R = MX1508(27, 26)
Sp= 512 #значение ШИМ-сигнала, подаваемого на драйвер двигателей(варируется от 0 до 1023), но лучше подбирать, чтобы датчики успевали срабатывать
Lt=60 #значение яркости светодиода
debug=1 #флаг отладки(0 - отладка отключена, 1 - включена)

R_W_count,W_count,col_id,direct,react,dist=0,0,0,0,0,500 #инициализация переменных
R_m_pin = Pin(23, Pin.IN) #подключение оптического энкодера
L_m_pin = Pin(34, Pin.IN)

motor_R.forward(Sp) #запустить двигатели
motor_L.forward(Sp)

def R_W_int(pin): #обработка вращения колес при помощи правого энкодера
    global W_count,R_W_count #глобальные переменные
    W_count+=1
    R_W_count+=1
    if direct==0: #движение вперёд
        if W_count>0:
            motor_R.forward(0)
            motor_L.forward(Sp)
        else:
            motor_R.forward(Sp)
            motor_L.forward(Sp)
    elif direct==1: #движение налево
        if W_count>0:
            motor_R.forward(0)
            motor_L.reverse(Sp)
        else:
            motor_R.forward(Sp)
            motor_L.reverse(Sp)
    elif direct==2: #движение направо
        if W_count>0:
            motor_R.reverse(0)
            motor_L.forward(Sp)
        else:
            motor_R.reverse(Sp)
            motor_L.forward(Sp)        
    elif direct==3: #движение назад
        if W_count>0:
            motor_R.reverse(0)
            motor_L.reverse(Sp)
        else:
            motor_R.reverse(Sp)
            motor_L.reverse(Sp)
    elif direct==-1: #стоим на месте
        motor_R.reverse(0)
        motor_L.reverse(0)
    
def L_W_int(pin): #обработка вращения колес при помощи левого энкодера
    global W_count
    W_count-=1
    if direct==0:
        if W_count<0:
            motor_R.forward(Sp)
            motor_L.forward(0)
        else:
            motor_R.forward(Sp)
            motor_L.forward(Sp)
    elif direct==1:
        if W_count>0:
            motor_R.forward(Sp)
            motor_L.reverse(0)
        else:
            motor_R.forward(Sp)
            motor_L.reverse(Sp)
    elif direct==2:
        if W_count>0:
            motor_R.reverse(Sp)
            motor_L.forward(0)
        else:
            motor_R.reverse(Sp)
            motor_L.forward(Sp)
    elif direct==3:
        if W_count>0:
            motor_R.reverse(Sp)
            motor_L.reverse(0)
        else:
            motor_R.reverse(Sp)
            motor_L.reverse(Sp)
    elif direct==-1:
        motor_R.reverse(0)
        motor_L.reverse(0)
    
R_m_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=R_W_int) #прерывания для срабатывания счётчиков энкодеров
L_m_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler=L_W_int)

async def W_sp(int_ms):
    global R_W_count,direct
    while 1:
        await asio.sleep_ms(int_ms) #оператор выхода
        if 150<dist<250:
            if dist%2:
                direct=1
            else:
                direct=2
            R_W_count=0    
            while R_W_count<5:   
                await asio.sleep_ms(0)
        elif dist<150:
            direct=3
            R_W_count=0 
            while R_W_count<10:   
                await asio.sleep_ms(0)
        else:
            direct=0  
        if col_id==4: #реакция на чёрную линию
            direct=2
            R_W_count=0 
            while R_W_count<5:   
                await asio.sleep_ms(0)
            direct=0
            R_W_count=0 
            while R_W_count<16:  
                await asio.sleep_ms(0)
        if col_id==0: #если указанный цвет найден
            react+=1
        if react == 3:
            direct = 0
        else:
            motor_R.reverse(Sp)
            motor_L.forward(Sp)   
                
async def color_det(int_ms):
    global color,col_id
    while 1:
        await asio.sleep_ms(int_ms)
        r,g,b=tcs.read(1)[0],tcs.read(1)[1],tcs.read(1)[2]
        h,s,v=rgb_to_hsv(r,g,b) #перевод из одного цветового пространства в другое
        if 0<h<50:
            col_id=0 #красный
        elif 50<h<70:
            col_id=1 #жёлтый
        elif 70<h<180:
            if v>5:
                col_id=2 #белый
            else:
                col_id=3 #зелёный
        if s<10 and v<4:
                col_id=4 #чёрный
        elif 181<h<250:
            if s>30:
                col_id=5 #голубой
            else:
                col_id=6 #синий
        elif 241<h<360:
            col_id=7 #фиолетовый
        if debug:
            print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))
            
async def dist_det(int_ms):
    global dist
    while(1):
        await asio.sleep_ms(int_ms)
        tof.start()
        dist=tof.read()-65
        tof.stop()
        if debug:
            print('Distance is {}. W_count {}'.format(dist,W_count))
            
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
        
# define loop
loop = asio.get_event_loop()

#create looped tasks
loop.create_task(color_det(0))
loop.create_task(dist_det(0))
loop.create_task(W_sp(0))
loop.create_task(LED_cont(0))
# loop run forever
loop.run_forever()
    