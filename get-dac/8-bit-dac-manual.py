import RPi.GPIO as GPIO
import time
dynamic_range=3.3
def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)
def number_to_dac(number,leds):
    GPIO.output(leds,[int(element) for element in bin(number) [2:].zfill(8)])


GPIO.setmode(GPIO.BCM)
dac_bits=[16,20,21,25,26,17,27,22]
dac_bits=dac_bits[::-1]
for led in dac_bits:
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,0)
try:
    while True:
        try:
            voltage = float(input("Введите напряжение:"))
            number = voltage_to_number(voltage)
            number_to_dac(number,dac_bits)
        except ValueError:
            print("Вы ввели не число. Попробуй еще раз\n")
finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()