import RPi.GPIO as GPIO #import RPi.GPIO module
from time import sleep #used to create delays

GPIO.setmode(GPIO.BCM) #choose BCM mode
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) #set GPIO 18 as output
GPIO.setup(22,GPIO.IN) #set GPIO 22 as input

while True: #loops the next 4 lines
    GPIO.output(18,1)
    if GPIO.input(22):
        GPIO.output(18,0) #output logic low/'0'
        break