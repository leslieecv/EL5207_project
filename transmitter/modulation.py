"""
Module for the transmitter
Made by: Fernanda Borja, Matías Bustos & Leslie Cárdenas
"""
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import coding as code

import sounddevice as sd
from scipy.io.wavfile import write, read

# Global variables
DURATION = 48 # seconds
SAMPLE_FREQ = 32000 # hertz
ANS_DIC = {"y":1, "n":0}
FREQUENCIES = [[1, 2], [3, 4]] # transmitter [image, text] CHANGE!!!!!!!!!!!



# space_freq: frequency for 0
# mark_freq: frequency for 1
# baud: bits per second
def bfsk_modulate(bit_array, space_freq, mark_freq, baud, sample_rate):
    seconds_per_bit = 1 / baud
    samples_per_bit = int(sample_rate * seconds_per_bit)
    t = np.linspace(0, seconds_per_bit, samples_per_bit)
    space = np.sin(space_freq * 2 * np.pi * t)
    mark = np.sin(mark_freq * 2 * np.pi * t)
    signal = np.array([])
    for bit in bit_array:
        if bit == 0:
            signal = np.append(signal, space)
        elif bit == 1:
            signal = np.append(signal, mark)
    return signal

# test
sig_010110 = bfsk_modulate([0,1,0,1,1,0], 8, 16, 1, 1000)
plt.plot(sig_010110)
plt.show()
