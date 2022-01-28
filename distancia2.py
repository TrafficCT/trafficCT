from machine import Pin
import time
from HCSR04 import HCSR04

#Definicion de pines led semaforo1
led_red = Pin(16, Pin.OUT)
led_orange = Pin(17, Pin.OUT)
led_green = Pin(5, Pin.OUT)
#Sensor que apunta hacia los vehiculos
sensor1 = HCSR04(trigger_pin=15, echo_pin=2, echo_timeout_us=10000)
#sensor detras semaforo
sensor2 = HCSR04(trigger_pin=33, echo_pin=32, echo_timeout_us=10000)
#sensor final de la calle
sensor3 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=10000)

def semaforo1_normal():
    
    led_red.value(1)
    time.sleep(5)
    led_orange.value(1)
    time.sleep(4)
    led_red.value(0)
    led_orange.value(0)
    led_green.value(1)
    time.sleep(15)
    led_green.value(0)
    led_orange.value(1)
    time.sleep(5)
    led_orange.value(0)
        
def semaforo1_trancon():
        
    led_red.value(1)
    time.sleep(20)
    led_orange.value(1)
    time.sleep(4)
    led_red.value(0)
    led_orange.value(0)
    led_green.value(1)
    time.sleep(8)
    led_green.value(0)
    led_orange.value(1)
    time.sleep(5)
    led_orange.value(0)
    
while True:      
      
        distance1 = int(sensor1.distance_cm())
        print("Sensor que apunta hacia los vehiculos :" ,distance1 , "cm")
        time.sleep_ms(10)
        
        distance2 = int(sensor2.distance_cm())
        print("sensor detras semaforo" ,distance2, "cm")
        time.sleep_ms(10)
        
        
        distance3 = int(sensor3.distance_cm())
        print("sensor final: " ,distance3, "cm")
        time.sleep_ms(10)
       
        
        if distance1 <= 80:
            semaforo1_normal()
            print("Hay presencia de Vehiculos")
            
        if distance2 <= 8:
            semaforo1_trancon() 
            print("Hay trancon")
            
        if distance3 <= 15:
            semaforo1_trancon() 
            print("Todavia sigue el trancon")
         
            

      