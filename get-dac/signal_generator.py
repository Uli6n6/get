import numpy
import time
import math
def get_sin_wave_amplitude(freq, t):
    phase=2*math.pi*freq*t
    raw_sin=math.sin(phase)
    normalized_amplitude=(raw_sin+1)/2
    return normalized_amplitude

def triangal(freq, t):
    y=((2/math.pi)*math.asin(math.sin(2*math.pi*freq*t))+1)/2
    return y

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)