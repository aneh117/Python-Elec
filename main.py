import RPi.GPIO as GPIO
import dht11
import time
import datetime
from time import sleep
import requests
import threading
from app import init_db
from app import send_fire_alert
from app import run_flask
import I2C_LCD_driver  # Import the library
LCD = I2C_LCD_driver.lcd()  # Instantiate an LCD object

TOKEN1 = "8128357121:AAF-1qgiCVYzbsQk00L13cJCc_zIptu6vZo"
chat_id1 = "5053817722"
message1 = "Temperature reaching dangerous level"
message2 = "Fire Detected, Attention Required"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  #buzzer
GPIO.setup(24, GPIO.OUT)  #led
GPIO.setup(22, GPIO.IN)   #switch
GPIO.setup(26,GPIO.OUT) #set GPIO 26 as output
PWM=GPIO.PWM(26,50) #set 50Hz PWM output at GPIO26

instance = dht11.DHT11(pin=21)  # read data using pin 21
result = instance.read()
flask_started = False

def threadingtemp(temperature, humidity):
         print("Uploaded temperature and humidity readings to thingspeak")
         resp=requests.get("https://api.thingspeak.com/update?api_key=I88GJ2CVBBW57XW4&field1=%s&field2=%s" %(result.temperature,result.humidity))
         sleep(20)
         
def monitor_temperature():
    global flask_started
    try:
        while True:  # keep reading, unless switch is on
            if GPIO.input(22):
                print("Switch is On")
                break

            result = instance.read()
            display_message("Temp: %-3.1f C" % result.temperature, "Humidity: %-3.1f %%" % result.humidity)
                

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

            if result.temperature > 27:
                GPIO.output(18, 1)
                GPIO.output(24, 1)
                PWM.start(12) #13% duty cycle
                print('duty cycle:', 12) #9 o'clock position
                sleep(4)
                GPIO.output(18, 0)
                GPIO.output(24, 0)
                sleep(1)
                url = f"https://api.telegram.org/bot{TOKEN1}/sendMessage?chat_id={chat_id1}&text={message2}"
                print(requests.get(url).json())
                send_fire_alert()

            if result.temperature < 26:
                PWM.start(3)
                print('duty cycle:', 3)
                sleep(4)
                
                
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()  

def display_message(line1, line2="", delay=1):
    """Displays a message on the LCD screen for a specified time."""
    LCD.lcd_clear()
    LCD.lcd_display_string(line1, 1)  # Display text on line 1
    LCD.lcd_display_string(line2, 2)  # Display text on line 2 (if any)
    sleep(delay)

if __name__ == "__main__":
  while True:
    init_db()

    
    if not flask_started:
        flask_started = True
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
    monitor_temperature()
    sleep(1)

           
       


              


