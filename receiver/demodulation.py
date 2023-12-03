"""
Module for the receptor
Made by: Fernanda Borja, Matías Bustos & Leslie Cárdenas
"""
# Import libraries
import decoding as decode
#
import scipy
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write, read
from scipy.signal import correlate
import matplotlib.pyplot as plt
from scipy import signal
import math
# Global variables
DURATION = 48 # seconds
SAMPLE_FREQ = 44100 # hertz
SYNC_FREQ = [[348, 894], [5298, 5792]] # 
FREQUENCIES = [
    [[1337, 1883],  # Text
     [2327, 2823],  # R
     [3317, 3813],  # G
     [4307, 4803]], # B   
    [[6287, 6783],  # Text  
     [9257, 9753],  # R
     [8267, 8763], # G
     [7277, 7773],]]# B   
BAUD = 40
ANS_DIC = {"y":1, "n":0}

"""
Recording function
Records and stores the data in a .wav file of a given name
"""
def record(seconds: int, fs: int, filename = "output.wav"):
    print(f"Recording with fs = {fs} for {seconds} s...")
    myrecording = sd.rec(int(seconds * fs), samplerate = fs, channels = 1) 
    sd.wait()  # Wait until recording is finished
    write(f'{filename}', fs, myrecording)
    print(f"Audio recorded and saved as {filename}")
    return
"""
Filtering function
"""
def filter_freq(signal, freq, window, fs = SAMPLE_FREQ, order = 5):
    filter = scipy.signal.butter(order, [freq - window, freq + window], "bandpass", fs = fs, output = "sos")
    filtered = scipy.signal.sosfiltfilt(filter, signal)
    return filtered

"""
Demodulation function
"""
def fsk_demodulate(raw_signal, space_freq, mark_freq, baud, sample_rate):
    seconds_per_bit = 1 / baud
    samples_per_bit = int(sample_rate * seconds_per_bit)
    t = np.linspace(0, seconds_per_bit, samples_per_bit)
    map = {
        '0': space_freq,
        '1': mark_freq
    }
    # maps from bit sequence (like "10") to the modulated wave representing that "symbol"
    wave_to_symbol_map = {bit_seq: np.sin(freq * 2 * np.pi * t) for bit_seq, freq in map.items()}
    
    bit_str = ""
    for index in range(0, len(raw_signal), samples_per_bit):
        best_symbol = ""
        highest_dot_abs = 0
        for symbol, symbol_wave in wave_to_symbol_map.items():
            raw_window = raw_signal[index:index+samples_per_bit]
            dot_abs = np.abs(np.dot(symbol_wave[0:len(raw_window)], raw_window))
            if dot_abs > highest_dot_abs:
                best_symbol = symbol
                highest_dot_abs = dot_abs
        bit_str += best_symbol
    return bit_str
"""
Sync function
Based on a sync pulse in a given freq, we set the start of each message 
"""
# Aux function, creator of reference
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

# Aux function, get two max index
def get_two_max_indices(arr):
    sorted_indices = np.argsort(arr)
    max_indices = sorted_indices[-2:]
    return max_indices
#
def sync_detect(audio, sync_freq, mode = "img"):
    # Filter in the frequency
    wave0 = filter_freq(audio, sync_freq[0], 50, SAMPLE_FREQ)
    wave1 = filter_freq(audio, sync_freq[1], 50, SAMPLE_FREQ)
    wave_sum = wave0 + wave1
    # get the reference
    ref_init = bfsk_modulate([1, 1, 1, 1], sync_freq[0], sync_freq[1], BAUD, SAMPLE_FREQ)
    ref_end = bfsk_modulate([0, 0, 0, 0], sync_freq[0], sync_freq[1], BAUD, SAMPLE_FREQ)
    # From this we get the peaks
    start = 0
    end = 0
    #
    corr_init = []
    corr_end = []
    for i in range(math.floor((len(wave_sum))/len(ref_init))):
        y_w = wave_sum[i* len(ref_init):(i+1) * len(ref_init)]
        cor = correlate(ref_init, y_w, mode='full', method='fft')
        corr_init.append(sum(cor**2))
        y_x = wave_sum[i* len(ref_end):(i+1) * len(ref_end)]
        cor = correlate(ref_end, y_x, mode='full', method='fft')
        corr_end.append(sum(cor**2)) 
    # return audio[start:end]
    if (mode == "img"):
        start = np.min(get_two_max_indices(corr_init))
        end = np.min(get_two_max_indices(corr_end))
    else: # text
        start = np.max(get_two_max_indices(corr_init))
        end = np.max(get_two_max_indices(corr_end))
        # print(end)
    # print(start, end)
    # Get the location in sample points
    samples_per_bit = int(SAMPLE_FREQ / BAUD)
    start = int((start + 1)*samples_per_bit*4)
    end = int((end)*samples_per_bit*4)
    # plt.plot(corr_init)
    # plt.show()
    # plt.plot(corr_end)
    # plt.show()
    # print(start, end)
    # print(len(audio) - start)
    return audio[start:end]

# Assembly of functions
def main():
    filename = 'D:\GitHub\EL5207_project\\2img_2txt_sync.wav'
    # listen
    # record(2, SAMPLE_FREQ, filename) 
    # read
    fs, audio = read(filename)
    titles = []
    for i in range(len(FREQUENCIES)):
        freqs = FREQUENCIES[i]
        wave = sync_detect(audio, SYNC_FREQ[i], mode="text")
        # Text
        text_wave0 = filter_freq(wave, freqs[0][0], 20, fs)
        text_wave1 = filter_freq(wave, freqs[0][1], 20, fs)
        wave_sum = text_wave0 + text_wave1
        text_bin = fsk_demodulate(wave_sum, freqs[0][0], freqs[0][1], BAUD, fs)
        decod = decode.Decoding(text_bin, mode='text')
        # print(text_bin[-10:])
        decod_ch = decod.decod_data
        print(decod_ch)
        titles.append(decod_ch)

    for i in range(len(FREQUENCIES)): # Both transmitters
        freqs = FREQUENCIES[i]
        wave = sync_detect(audio, SYNC_FREQ[i], mode="img")
        # Image
        # Red channel
        r_wave0 = filter_freq(wave, freqs[1][0], 20, fs)
        r_wave1 = filter_freq(wave, freqs[1][1], 20, fs)
        r_sum = r_wave0 + r_wave1
        r_bin = fsk_demodulate(r_sum, freqs[1][0], freqs[1][1], BAUD, fs)
        # print(r_bin)
        # Green channel
        g_wave0 = filter_freq(wave, freqs[2][0], 20, fs)
        g_wave1 = filter_freq(wave, freqs[2][1], 20, fs)
        g_sum = g_wave0 + g_wave1
        g_bin = fsk_demodulate(g_sum, freqs[2][0], freqs[2][1], BAUD, fs)
        # Blue channel
        b_wave0 = filter_freq(wave, freqs[3][0], 20, fs)
        b_wave1 = filter_freq(wave, freqs[3][1], 20, fs)
        b_sum = b_wave0 + b_wave1
        b_bin = fsk_demodulate(b_sum, freqs[3][0], freqs[3][1], BAUD, fs)
        # Image Assembly c:
        # print(len(r_bin), len(g_bin), len(b_bin))
        colorlist = [r_bin, g_bin, b_bin]
        decod = decode.Decoding(colorlist, mode='image')
        decod_ch = decod.decod_data
        plt.imshow(decod_ch, cmap='gray')
        plt.title(titles[i], fontsize=20)
        plt.axis('off')
        # plt.savefig(f"result{1 + i}.pdf", bbox_inches='tight')
        plt.show()
        plt.clf() 
    pass


if __name__ == "__main__":
    print("-------------Receiver Module-------------")
    # start = input("Start receiving data? [y/n]: ")
    if True:#(ANS_DIC[start]):
        main()
    else:
         pass
    
