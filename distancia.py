from machine import Pin, I2C
import utime
import sh1106
from HCSR04 import HCSR04


ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = sh1106.SH1106_I2C(ancho, alto, i2c)

#print(i2c.scan())

sensor = HCSR04(trigger_pin=18, echo_pin=14, echo_timeout_us=10000)

while True:
    
    oled.fill(0)
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
    utime.sleep(1)
    
    oled.text("DISTANCIA", 25, 10)
    oled.text(str(int(distance)), 50, 25)
    oled.text('CM',68,25)
    oled.fill_rect(1, 40, int(distance), 43, 1)
    oled.show()
    utime.sleep_ms(50)
    
    
if _name==("main_"):
    main()