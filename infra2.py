from machine import Pin
import utime

sensor8 = Pin(25, Pin.IN, Pin.PULL_DOWN)
sensor9 = Pin(9, Pin.IN, Pin.PULL_DOWN)
sensor10 = Pin(13, Pin.IN, Pin.PULL_DOWN)
    

while True:
    estado1 = sensor8.value()#cerca al semaforo - primer sensor   
    estado2 = sensor9.value()#segundo sensor - del medio
    estado3 = sensor10.value()#sensor final -tercer
 
    
    if estado1 == 0 and estado2 == 1 and estado3 == 1:
        print("Transito Normal")
        print("Este es el valor del estado 1 : " , estado1)
        print("Este es el valor del estado 2 : " , estado2)
        print("Este es el valor del estado 3 : " , estado3)
        
    elif estado1 == 0 and estado2 == 0  and estado3 == 1:
        print("Trancon a nivel medio")
        print("Este es el valor del estado 1 : " , estado1)
        print("Este es el valor del estado 2 : " , estado2)
        print("Este es el valor del estado 3 : " , estado3)
       
    elif estado1 == 0 and estado2 == 0  and estado3 == 0:
        print("Trancon")
        print("Este es el valor del estado 1 : " , estado1)
        print("Este es el valor del estado 2 : " , estado2)
        print("Este es el valor del estado 3 : " , estado3)
    else:
        print("Via Libre")
        print("Este es el valor del estado 1 : " , estado1)
        print("Este es el valor del estado 2 : " , estado2)
        print("Este es el valor del estado 3 : " , estado3)   
        
