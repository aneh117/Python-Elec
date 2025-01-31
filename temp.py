import RPi.GPIO as GPIO
import dht11
import time
import datetime
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT) #set GPIO 18 as output
GPIO.setup(24,GPIO.OUT) #set GPIO 24 as output

instance = dht11.DHT11(pin=21) #read data using pin 21

try:
    while True: #keep reading, unless keyboard is pressed
        result = instance.read()
        if result.is_valid(): #print datetime & sensor values
            print("Last valid input: " +     
                str(datetime.datetime.now()))
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
        time.sleep(0.5) #short delay between reads

        if result.temperature > 26:
            GPIO.output(18,1)
            GPIO.output(24,1)
            sleep(1)
            GPIO.output(18,0)
            GPIO.output(24,0)
            sleep(1)
        if result.temperature> 27:
            GPIO.output(18,1)
            GPIO.output(24,1)
            sleep(4)
            GPIO.output(18,0)
            GPIO.output(24,0)
            sleep(1)
            
            
        
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup() #Google what this means…


