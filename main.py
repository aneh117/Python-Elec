import RPi.GPIO as GPIO
import dht11
import time
import datetime
from time import sleep
import requests
import threading

TOKEN1 = "8128357121:AAF-1qgiCVYzbsQk00L13cJCc_zIptu6vZo"
TOKEN2 = "7547168681:AAFOMetVjyTejjOEjKfVMRBv0EJ68nJ6Sb0"
chat_id1 = "5053817722"
chat_id2 = "6267940035"
message1 = "Temperature reaching dangerous level"
message2 = "Fire Detected, Attention Required!!!"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # set GPIO 18 as output
GPIO.setup(24, GPIO.OUT)  # set GPIO 24 as output
GPIO.setup(22, GPIO.IN)   # set GPIO 22 as input

instance = dht11.DHT11(pin=21)  # read data using pin 21
result = instance.read()

def threadingtemp():
    if temperature is not None and humidity is not None:
         resp=requests.get("https://api.thingspeak.com/update?api_key=I88GJ2CVBBW57XW4&field1=%s&field2=%s" %(result.temperature,result.humidity))
         sleep(15)


def monitor_temperature():
    try:
        while True:  # keep reading, unless keyboard is pressed
            if GPIO.input(22):
                break

            
            if result.is_valid():  # print datetime & sensor values
                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %-3.1f C" % result.temperature)
                print("Humidity: %-3.1f %%" % result.humidity)
                thingspeak_thread = threading.Thread(target=threadingtemp, args=(result.temperature, result.humidity))
                thingspeak_thread.start()
                
            
            time.sleep(0.5)  # short delay between reads

            if result.temperature > 26:
                GPIO.output(18, 1)
                GPIO.output(24, 1)
                sleep(1)
                GPIO.output(18, 0)
                GPIO.output(24, 0)
                sleep(1)
                url = f"https://api.telegram.org/bot{TOKEN1}/sendMessage?chat_id={chat_id1}&text={message1}"
                print(requests.get(url).json())

            if result.temperature > 28:
                GPIO.output(18, 1)
                GPIO.output(24, 1)
                sleep(4)
                GPIO.output(18, 0)
                GPIO.output(24, 0)
                sleep(1)
                url1 = f"https://api.telegram.org/bot{TOKEN1}/sendMessage?chat_id={chat_id1}&text={message2}"
                url = f"https://api.telegram.org/bot{TOKEN2}/sendMessage?chat_id={chat_id2}&text={message2}"
                print(requests.get(url).json())
                print(requests.get(url1).json())

    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()  # Google what this means…
        
while True:
    monitor_temperature()
    sleep(1)


