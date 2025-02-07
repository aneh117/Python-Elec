import RPi.GPIO as GPIO
import dht11
import time
import datetime
from time import sleep
import requests
TOKEN1 = "8128357121:AAF-1qgiCVYzbsQk00L13cJCc_zIptu6vZo"
chat_id1 = "5053817722"
message1 = "Temperature reaching dangerous level"
Message2 = "Fire Detected, Attention Required!!!"

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
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id1}&text={message1}"
            print(requests.get(url).json())

        if result.temperature> 27:
            GPIO.output(18,1)
            GPIO.output(24,1)
            sleep(4)
            GPIO.output(18,0)
            GPIO.output(24,0)
            sleep(1)
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id1}&text={Message2}"
            print(requests.get(url).json())
            
            
        
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup() #Google what this means…


