import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range,verbose=False):
        GPIO.setmode(GPIO.BCM)
        self.gpio_bits = gpio_pin
        self.dynamic_range = dynamic_range
        self.verbose=verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits,GPIO.OUT, initial = 0)
        self.pwm_frequency=pwm_frequency
        self.pwm=GPIO.PWM(self.gpio_bits,self.pwm_frequency)
        self.pwm.start(self.pwm_frequency)

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            return 0
        self.pwm.ChangeDutyCycle(voltage / self.dynamic_range * 10)


    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()


GPIO.setmode(GPIO.BCM)

dac_bits=[16,20,21,25,26,17,27,22]
dac_bits=dac_bits[::-1]
for led in dac_bits:
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,0)


dac = PWM_DAC(12,10, 3.290,True)
while True:
    try:
        voltage = float(input("Введите напряжение:"))
        dac.set_voltage(voltage)
    except ValueError:
        print("Вы ввели не число. Попробуй еще раз\n")
dac.deinit()