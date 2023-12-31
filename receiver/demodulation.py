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
DURATION = 135 # seconds
SAMPLE_FREQ = 44100 # hertz
SYNC_FREQ = [[348, 894], [5298, 5792]] # 
FREQUENCIES = [
    [[1337, 3317],  # Text
     [1883, 3813],  # R
     [2327, 4307],  # G
     [2823, 4803]], # B
    [[6287, 8267],  # Text
     [6783, 8763],  # R
     [7277, 9257], # G
     [7773, 9753],]] # B
BAUD = 36
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
    wave0 = filter_freq(audio, np.mean(sync_freq), np.mean(sync_freq)/2, SAMPLE_FREQ)
    # _, _, _, _ = plt.specgram(wave0, Fs = SAMPLE_FREQ, scale = 'linear')
    # plt.show()
    # wave1 = filter_freq(audio, sync_freq[1], 50, SAMPLE_FREQ)
    wave_sum = wave0 #+ wave1
    # get the reference
    points = np.linspace(0, 1, int(SAMPLE_FREQ*1))
    init0 = signal.chirp(points, sync_freq[0], 1, np.mean(sync_freq))
    init1 = signal.chirp(points, sync_freq[1], 1, np.mean(sync_freq))
    ref_init = init0
    ref_end = init1
    start = 0
    end = 0
    corr_init = np.abs(correlate(wave_sum, ref_init, mode='valid', method='fft'))
    corr_end = np.abs(correlate(wave_sum, ref_end, mode='valid', method='fft'))
    samples_per_bit = int(SAMPLE_FREQ / BAUD)
    # Find peaks
    if (mode == "img"):
        start, _ = signal.find_peaks(corr_init, distance = 44100, height = (np.max(corr_init)*0.4, np.max(corr_init)))
        start = start[0]
        end, _ = signal.find_peaks(corr_end, distance = 44100, height = (np.max(corr_end)*0.4, np.max(corr_end)))
        end = end[0]
        while ((end - (start + len(ref_init)))%(samples_per_bit*8) != 0):
            if ((end - (start + len(ref_init)))%(samples_per_bit*8) > (samples_per_bit*4)):
                end+=1
            else:
                end-=1
  
    else: # text
        start, _ = signal.find_peaks(corr_init, distance = 44100, height = (np.max(corr_init)*0.8, np.max(corr_init)))
        # print(start)
        start = start[1]
        end, _ = signal.find_peaks(corr_end, distance = 44100, height = (np.max(corr_end)*0.8, np.max(corr_end)))
        # print(end)
        end = end[1]

        while ((end - (start + len(ref_init)))%(samples_per_bit*8) != 0):
            if ((end - (start + len(ref_init)))%(samples_per_bit*8) > (samples_per_bit*4)):
                end+=1
            else:
                end-=1
        # print(f"La ventana con correlacion maxima parte en {start} y termina en {end}")
    # Get the location in sample points
    bit_start = start
    bit_end = end
    # np.save("enviar.npy", corr_end)
    # plt.plot(corr_init, "o")
    # plt.plot(corr_end, "o")
    # plt.savefig(f"test_{mode}.png", dpi = 300)
    # plt.show()
    # plt.clf()
    # print(bit_start, bit_end)
    return audio[bit_start + len(ref_init) :bit_end]

# Assembly of functions
def main():
    filename = 'D:\GitHub\EL5207_project\\tests\\fourthtest36.wav'
    # listen
    # record(DURATION, SAMPLE_FREQ, filename) 
    # read
    fs, audio = read(filename)
    # f1 = 'd:\\test360.wav'
    # f2 = 'd:\\test361.wav'
    # fs, audio1 = read(f1)
    # fs, audio2 = read(f2)
    # audio2 = np.append(np.zeros(len(audio1) - len(audio2)), audio2)
    # print(type(audio1))
    # audio = audio1  + audio2
    # print(len(audio))

    
    titles = []
    for i in range(len(FREQUENCIES)):
        
        freqs = FREQUENCIES[i]
        wave = sync_detect(audio, SYNC_FREQ[i], mode="text")
        # Text
        text_wave0 = filter_freq(wave, freqs[0][0], 100, fs)
        text_wave1 = filter_freq(wave, freqs[0][1], 100, fs)
        wave_sum = text_wave0 + text_wave1
        text_bin = fsk_demodulate(wave_sum, freqs[0][0], freqs[0][1], BAUD, fs)
        print(type(text_bin))
        # np.save(f'bins/received_txt{i+1}.npy', text_bin)
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
        r_wave0 = filter_freq(wave, freqs[1][0], 100, fs)
        r_wave1 = filter_freq(wave, freqs[1][1], 100, fs)
        r_sum = r_wave0 + r_wave1
        r_bin = fsk_demodulate(r_sum, freqs[1][0], freqs[1][1], BAUD, fs)
        # np.save(f'bins/received_rch{i+1}.npy', r_bin)
        # print(r_bin)
        # Green channel
        g_wave0 = filter_freq(wave, freqs[2][0], 100, fs)
        g_wave1 = filter_freq(wave, freqs[2][1], 100, fs)
        g_sum = g_wave0 + g_wave1
        g_bin = fsk_demodulate(g_sum, freqs[2][0], freqs[2][1], BAUD, fs)
        # np.save(f'bins/received_gch{i+1}.npy', g_bin)
        # Blue channel
        b_wave0 = filter_freq(wave, freqs[3][0], 100, fs)
        b_wave1 = filter_freq(wave, freqs[3][1], 100, fs)
        b_sum = b_wave0 + b_wave1
        b_bin = fsk_demodulate(b_sum, freqs[3][0], freqs[3][1], BAUD, fs)
        # np.save(f'bins/received_bch{i+1}.npy', b_bin)
        # Image Assembly c:
        # print(len(r_bin), len(g_bin), len(b_bin))
        colorlist = [r_bin, g_bin, b_bin]
        decod = decode.Decoding(colorlist, mode='image')
        decod_ch = decod.decod_data
        plt.imshow(decod_ch, cmap='gray')
        plt.title(titles[i], fontsize=20)
        plt.axis('off')
        plt.savefig(f"exp_result{1 + i}.pdf", bbox_inches='tight')
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
    
