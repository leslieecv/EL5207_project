"""
Module for the transmitter
Made by: Fernanda Borja, Matías Bustos & Leslie Cárdenas
"""
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

import soundfile as sf
from scipy.io.wavfile import write, read

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

# test hola en binario
sig_010110 = bfsk_modulate([0,1,1,0,1,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,0,0,1,1,0,0,0,0,1], 1337, 1883, 5, 44100)
plt.plot(sig_010110)
plt.show()

# exportar audio en wav
sf.write("hola.wav",sig_010110, 44100)