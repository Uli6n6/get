import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10,6))
    plt.plot(time,voltage)
    plt.title('График зависимости напряжения на входе АЦП от времени', fontsize=12, fontweight = 'bold')
    plt.xlabel('Время, с',fontsize=12)
    plt.ylabel('Напряжение, В',fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()

def plot_sampling_period_hist(time_values):
    delta_time=list()
    for i in range(len(time_values)-1):
        delta_time.append(time_values[i+1]-time_values[i])
    plt.figure(figsize=(10,6))
    plt.hist(delta_time)
    plt.title('Распределение периодов дискретизации измерений по времени на одно измерение', fontsize=12, fontweight = 'bold')
    plt.xlabel('Период измерений, с',fontsize=12)
    plt.ylabel('Количество измерений+',fontsize=12)
    plt.xlim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)
    
    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self,number):
        GPIO.output(self.bits_gpio,[int(element) for element in bin(number) [2:].zfill(8)])


    def sequential_counting_adc(self):
        for i in range(1,256):
            self.number_to_dac(i)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                return i
        return 255

    def get_sc_voltage(self):
        return self.sequential_counting_adc()*(self.dynamic_range/255) 

    def successive_approximation_adc(self):
        value = 0
        for bit in range(7,-1,-1):
            value_to_check = value + 2**bit
            self.number_to_dac(value_to_check)
            time.sleep(self.compare_time)
            comparator_result = GPIO.input(self.comp_gpio)
            if comparator_result == 0:
                value = value_to_check
        return value    

    def get_sar_voltage(self):
        return self.successive_approximation_adc()*(self.dynamic_range/255) 



try:
    start=time.time()
    voltage_value = list()
    time_values = list()
    duration = 10.0
    dac = R2R_ADC(3.1, compare_time = 0.0001, verbose = False)
    while time.time()-start<duration:

        try:
            voltage = dac.get_sc_voltage()
            time_values.append(time.time()-start)
            voltage_value.append(voltage)
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("хрень какая-то\n")
   
    plot_voltage_vs_time(time_values, voltage_value, 3.1)
    plot_sampling_period_hist(time_values)
    
finally:
    dac.deinit()