import smbus
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
        delta_time.append(time_values[i+1]-time_values[i]-1)
    plt.figure(figsize=(10,6))
    plt.hist(delta_time)
    plt.title('Распределение периодов дискретизации измерений по времени на одно измерение', fontsize=12, fontweight = 'bold')
    plt.xlabel('Период измерений, с',fontsize=12)
    plt.ylabel('Количество измерений+',fontsize=12)
    plt.xlim(0, 0.1)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()

class MCP3021:
    def __init__(self, dynamic_range,verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_i2c_block_data(self.address, 0, 2)        
        lower_data_byte = data[1]
        upper_data_byte = data[0]
        number = ((upper_data_byte & 0x0F) << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f'Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}')
        return number

    def get_voltage(self):
        return self.get_number()*(self.dynamic_range/1023)

 


try:
    start=time.time()
    voltage_value = list()
    time_values = list()
    duration = 30.0
    dac = MCP3021(3.0)
    while time.time()-start<duration:

        try:
            voltage = dac.get_voltage()
            time_values.append(time.time()-start)
            voltage_value.append(voltage)
            time.sleep(1)
        except KeyboardInterrupt:
            print("хрень какая-то\n")
    plot_voltage_vs_time(time_values, voltage_value, 3.0)
    plot_sampling_period_hist(time_values)
    
finally:
    dac.deinit()      