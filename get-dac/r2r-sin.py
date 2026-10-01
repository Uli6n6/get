import signal_generator as sg
import time
import RPi.GPIO as GPIO
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
        GPIO.output(self.gpio_bits,[int(element) for element in bin(number) [2:].zfill(8)])

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            return 0
        return self.set_number(int(voltage / self.dynamic_range * 255))
amplitude =2
signal_frequency = 10
sampling_frequency = 6000
start_time=time.time()
GPIO.setmode(GPIO.BCM)
dac_bits=[16,20,21,25,26,17,27,22]

try:
    dac=R2R_DAC(dac_bits, 3.0)
    while True:
        sg.wait_for_sampling_period(sampling_frequency)
        dac.set_voltage(sg.get_sin_wave_amplitude(signal_frequency, time.time()-start_time)*amplitude)

finally:
    dac.deinit()