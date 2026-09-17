import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led=26
GPIO.setup(led, GPIO.OUT)
state=0.0
pwm=GPIO.PWM(led,200)
pwm.start(state)
period=5.0
botton=13
foto=6
GPIO.setup(botton, GPIO.IN)
GPIO.setup(foto, GPIO.IN)
while True:
    pwm.ChangeDutyCycle(state)
    time.sleep(0.5)
    state=state+1.0
    if state>100.0:
        state=0.0
        time.sleep(1)