
import signal_generator as sg
import time
import RPi.GPIO as GPIO
class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range,verbose=False):
        GPIO.setmode(GPIO.BCM)
        self.gpio_bits = gpio_pin
        self.dynamic_range = dynamic_range
        self.verbose=verbose
        GPIO.setup(gpio_pin,GPIO.OUT, initial = 0)
        self.pwm_frequency=pwm_frequency
        self.pwm=GPIO.PWM(self.gpio_bits,self.pwm_frequency)
        self.pwm.start(0)

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.0 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            return 0
        self.pwm.ChangeDutyCycle(voltage / self.dynamic_range * 100)


    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()




amplitude =3
signal_frequency = 5
sampling_frequency = 200
start_time=time.time()
dac=PWM_DAC(12,500, 3.1,True)
try:
    while True:
        sg.wait_for_sampling_period(sampling_frequency)
        dac.set_voltage(sg.triangal(signal_frequency, time.time()-start_time)*amplitude)
        

finally:
    dac.deinit()