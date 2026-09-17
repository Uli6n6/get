import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led=26
GPIO.setup(led, GPIO.OUT)
state=0
period=5.0
botton=13
GPIO.setup(botton, GPIO.IN)
while True:
    if GPIO.input(botton):
        state=not state
        GPIO.output(led,state)
        time.sleep(period)