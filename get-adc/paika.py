import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

CHARGE_PIN = 14
CHARGE_TIME = 45.0
DISCHARGE_TIME = 45.0
SAMPLE_DT = 0.01
DYNAMIC_RANGE = 5.0
MCP_ADDR = 0x4D


class MCP3021:
    def __init__(self, dynamic_range, address=MCP_ADDR, verbose=False):
        self.bus = SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = address
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        # MCP3021: 2 байта, старшие 4 бита первого байта = 0,
        # значащие 10 бит: (msb & 0x0F) << 6 | (lsb >> 2)
        data = self.bus.read_i2c_block_data(self.address, 0, 2)
        msb, lsb = data[0], data[1]
        number = ((msb & 0x0F) << 6) | (lsb >> 2)
        if self.verbose:
            print(f"data={data}, msb={msb:#04x}, lsb={lsb:#04x}, n={number}")
        return number

    def get_voltage(self):
        return self.get_number() * (self.dynamic_range / 1023.0)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHARGE_PIN, GPIO.OUT, initial=0)
    adc = MCP3021(DYNAMIC_RANGE)

    t_list, u_list = [], []
    start = time.time()

    try:
        # Фаза 1: зарядка
        print("Зарядка...")
        GPIO.output(CHARGE_PIN, 1)
        t_end = start + CHARGE_TIME
        while time.time() < t_end:
            try:
                u = adc.get_voltage()
            except OSError as e:
                print(f"I2C error: {e}")
                time.sleep(0.05)
                continue
            t_list.append(time.time() - start)
            u_list.append(u)
            time.sleep(SAMPLE_DT)

        # Фаза 2: разряд
        print("Разряд...")
        GPIO.setup(CHARGE_PIN, GPIO.IN)
        t_end = time.time() + DISCHARGE_TIME
        while time.time() < t_end:
            try:
                u = adc.get_voltage()
            except OSError as e:
                print(f"I2C error: {e}")
                time.sleep(0.05)
                continue
            t_list.append(time.time() - start)
            u_list.append(u)
            time.sleep(SAMPLE_DT)

    except KeyboardInterrupt:
        print("\nПрервано")
    finally:
        if GPIO.gpio_function(CHARGE_PIN) == GPIO.OUT:
            GPIO.output(CHARGE_PIN, 0)
        GPIO.cleanup()
        adc.deinit()

    plt.figure(figsize=(10, 6))
    plt.plot(t_list, u_list)
    plt.axvline(CHARGE_TIME, color='r', linestyle='--', label='Питание отключено')
    plt.title('Напряжение на конденсаторе: заряд → разряд',
              fontsize=12, fontweight='bold')
    plt.xlabel('Время, с', fontsize=12)
    plt.ylabel('Напряжение, В', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()