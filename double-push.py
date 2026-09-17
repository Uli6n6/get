import RPi.GPIO as GPIO
import time
def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]
GPIO.setmode(GPIO.BCM)
leds=[24,22,23,27,17,25,12,16]
for led in leds:
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,0)
GPIO.setup(9,GPIO.IN)
GPIO.setup(10,GPIO.IN)
n=0
while True:

    if GPIO.input(9)>0 and GPIO.input(10)>0:
        for led in leds:
            GPIO.output(led,1)
        time.sleep(1)
    if GPIO.input(9)>0:
        n+=1
        GPIO.output(leds,dec2bin(abs(n)%256))
        time.sleep(0.2)
    if GPIO.input(10)>0:
        
        n-=1
        print(n,dec2bin(abs(n)))
        GPIO.output(leds,dec2bin(abs(n)%256))
        time.sleep(0.2)
    