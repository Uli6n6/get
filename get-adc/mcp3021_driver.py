import smbus
import time
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
    dac = MCP3021(3.0)
    while True:
        try:
            voltage = dac.get_voltage()
            print(voltage,"B")
            time.sleep(1)
        except KeyboardInterrupt:
            print("хрень какая-то\n")
            dac.deinit()
            
finally:
    dac.deinit()        