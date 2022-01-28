#Aqui se define Modulos
from machine import Pin, I2C
import _thread
import network, time, urequests, sh1106
from HCSR04 import HCSR04
import bluetooth
from BLE import BLEUART
from utelegram import Bot

#Pantalla oled
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = sh1106.SH1106_I2C(ancho, alto, i2c)


#print(i2c.scan())
#Definicion de pines led semaforo1
led_red = Pin(16, Pin.OUT)
led_orange = Pin(17, Pin.OUT)
led_green = Pin(5, Pin.OUT)
#Definicion de pines led semaforo2
led_red1 = Pin(12, Pin.OUT)
led_orange1 = Pin(14, Pin.OUT)
led_green1 = Pin(23, Pin.OUT)

#Sensores medidores de distancia
#Sensor que apunta hacia los vehiculos
sensor1 = HCSR04(trigger_pin=15, echo_pin=2, echo_timeout_us=10000)
#sensor detras semaforo
sensor2 = HCSR04(trigger_pin=33, echo_pin=32, echo_timeout_us=10000)
#sensor final de la calle
sensor3 = HCSR04(trigger_pin=27, echo_pin=26, echo_timeout_us=10000)

#Aqui se define los sensores infrarrojos
sensor8 = Pin(25, Pin.IN, Pin.PULL_DOWN)
sensor9 = Pin(9, Pin.IN, Pin.PULL_DOWN)
sensor10 = Pin(13, Pin.IN, Pin.PULL_DOWN)

TOKEN = '5134278486:AAGBhSrDRE2V-cpFe-yXIXLh5mhlUmAo7gc'

bot = Bot(TOKEN)


def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

def leds(a,b,c,d,e,f):#Definicion de las luces de los semaforos 
    led_red.value(a)
    led_orange.value(b)
    led_green.value(c)
    led_red1.value(d)
    led_orange1.value(e)
    led_green1.value(f)

if conectaWifi ("ReydeCopas666", "Nacional666"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    
    #urls web para visualizar y enviar datos       
    url = "https://api.thingspeak.com/update?api_key=SU2ZYYLLO64E9T3I"
    url2 = "https://maker.ifttt.com/trigger/Sensores_Viales/with/key/fNXWcHIsaY2loe4IjXi1rvbBIcah3VUfD1wrgKKVPo?"  # la de drive
    
    #bot de telegram
    '''@bot.add_message_handler('Hola, como estas?')
    def help(update):
        update.reply('Necesitas controlar el transito con los semaforos?')

    @bot.add_message_handler('Value')
    def value(update):
        if leds.value():
            update.reply(estado_sem, estado_sem1, estado_sem2)
        else:
            update.reply(estado_sem, estado_sem1, estado_sem2)

    @bot.add_message_handler('Cual semaforo necesita ralentizar?')
    def on(update):        
        
            
    
    bot.start_loop()'''
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def nucleo_dos_semaforo():
        
        estado_sem = sensor8.value()#sensor frente al semaforo
        estado_sem1 = sensor9.value()#sensor en medio de la calle
        estado_sem2 = sensor10.value()#sensor al final de la calle
        print(estado_sem, estado_sem1, estado_sem2)
        time.sleep(0.01)
        
            
        while True:
            
            if estado_sem == 0 and estado_sem1 == 0 and  estado_sem2 == 0:
                 
                leds(1,0,0,0,0,1)#encendido semaforo 1 rojo y semaforo 2 en verde
                time.sleep(8)
                leds(0,1,0,0,1,0)#encendido semaforo 1 naranja y semaforo 2 en naranja
                time.sleep(4)
                leds(0,0,1,1,0,0)#encendido semaforo 1 naranja y semaforo 2 en naranja
                time.sleep(12)
                leds(0,1,0,0,1,0)#encendido semaforo 1 naranja y semaforo 2 en naranja
                time.sleep(4)
                 
            else:
                
                leds(1,0,0,0,0,1)#encendido semaforo 1 rojo y semaforo 2 en verde
                time.sleep(12)
                leds(0,1,0,0,1,0)#encendido semaforo 1 naranja y semaforo 2 en naranja
                time.sleep(4)
                leds(0,0,1,1,0,0)#encendido semaforo 1 naranja y semaforo 2 en naranja
                time.sleep(8)
                leds(0,1,0,0,1,0)#encendido semaforo 1 naranja y semaforo 2 en naranja
                time.sleep(12)
            
        

    _thread.start_new_thread(nucleo_dos_semaforo,())


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    while True:
        
        estado1 = sensor8.value()#cerca al semaforo - primer sensor
        estado2 = sensor9.value()#segundo sensor - del medio
        estado3 = sensor10.value()#sensor final -tercer
        time.sleep_ms(400)
        
        if estado1 == 1 and estado2 == 1 and estado3 == 1:
        
            print("Via Libre", estado1, estado2, estado3)
        
        if (estado1 == 0 and estado2 == 1 and estado3 == 1) or (estado1 == 0 and estado2 == 0  and estado3 == 1):
       
            print("Algunos Vehiculos en la Via", estado1, estado2, estado3)
                
        if (estado1 == 1 and estado2 == 0 and estado3 == 1) or (estado1 == 1 and estado2 == 0 and estado3 == 0) or (estado1 == 1 and estado2 == 1 and estado3 == 0) or (estado1 == 0 and estado2 == 1 and estado3 == 0):
        
            print("Posible Choque", estado1, estado2, estado3)
    
        if estado1 == 0 and estado2 == 0 and estado3 == 0:
      
            print("Trancon", estado1, estado2, estado3)
            
            
        distance1 = int(sensor1.distance_cm())
        print("Sensor que apunta hacia los vehiculos :" ,distance1 , "cm")
        time.sleep_ms(10)
        
        distance2 = int(sensor2.distance_cm())
        print("sensor detras semaforo" ,distance2, "cm")
        time.sleep_ms(10)
        
        
        distance3 = int(sensor3.distance_cm())
        print("sensor final: " ,distance3, "cm")
        time.sleep_ms(10)
       
        
        if distance1 <= 10:
            print("Hay vehiculos frente al semaforo")
            
        elif distance2 <=9:
            print("Hay trancon y represamiento en todas la vias")
            
        elif distance3 <= 13:
            print("Trancon va mas de una cuadra")
        
        else:
            print("Via Libre")
            
        #visualizacion de los datos en la oled
        oled.fill(0)
        oled.text("D1: ", 0, 0)
        oled.text(str(distance1), 60, 0)
        oled.text("D2: ", 0, 10)
        oled.text(str(distance2), 60, 10)
        oled.text("D3: ", 0, 20)
        oled.text(str(distance3), 60, 20)
        
        oled.show()
        
        #aqui se define la visualizacion en thingspeak
        respuesta = urequests.get(url+"&field1="+str(distance1)+"&field2="+str(distance2)+"&field3="+str(distance3))
        print(respuesta.text)
        print (respuesta.status_code)
        respuesta.close()
        #aqui se define el envio por medio de gmail
        respuesta2 = urequests.get(url2+"&value1="+ str("Hay_mucho_flujo_de_autos,_coja_otra_ruta ", distance2))
        print(respuesta2.text)
        print (respuesta2.status_code)
        respuesta2.close()
        
    
else:
    print ("Imposible conectar")
    miRed.active (False)    
             