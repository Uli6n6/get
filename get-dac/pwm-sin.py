
import signal_generator as sg
import time
import RPi.GPIO as GPIO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range,verbose=False):
        GPIO.setmode(GPIO.BCM)
        self.gpio_bits = gpio_pin
        self.dynamic_range = dynamic_range
        self.verbose=verbose
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




amplitude =2
signal_frequency = 10000
sampling_frequency = 1000
start_time=time.time()
GPIO.setmode(GPIO.BCM)

try:
    dac=PWM_DAC(16,100, 3.0,True)
    while True:
        sg.wait_for_sampling_period(sampling_frequency)
        dac.set_voltage(sg.get_sin_wave_amplitude(signal_frequency, time.time()-start_time)*amplitude)

finally:
    dac.deinit()