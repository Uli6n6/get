import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose=verbose
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits,GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self,number):
        GPIO.output(gpio_bits,[int(element) for element in bin(number) [2:].zfill(8)])

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            return 0
        return int(voltage / self.dynamic_range * 255)
    
GPIO.setmode(GPIO.BCM)
dac_bits=[16,20,21,25,26,17,27,22]
dac_bits=dac_bits[::-1]
for led in dac_bits:
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,0)

try:
    dac = R2R_DAC(dac_bits, 3.183,True)
    while True:
        try:
            voltage = float(input("Введите напряжение:"))
            dac.set_voltage(voltage)
        except ValueError:
            print("Вы ввели не число. Попробуй еще раз\n")
finally:
    dac.deinit()