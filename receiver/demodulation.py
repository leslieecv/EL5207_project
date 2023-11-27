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
# Global variables
DURATION = 48 # seconds
SAMPLE_FREQ = 32000 # hertz
SYNC_FREQ = [1, 2] # MODIFY
FREQUENCIES = [[1, 1, 1, 2], [3, 3, 3, 4]] # transmitter [imageB, imageG, imageR, text] CHANGE!!!!!!!!!!!
SYMBOL_FREQ = 3
ANS_DIC = {"y":1, "n":0}

"""
Recording function
Records and stores the data in a .wav file of a given name
"""
def record(seconds: int, fs: int, filename = "output.wav"):
    print(f"Recording with fs = {fs} for {seconds} s...")
    myrecording = sd.rec(int(seconds * fs), samplerate = fs, channels = 2)
    sd.wait()  # Wait until recording is finished
    write(f'{filename}', fs, myrecording)
    print("Audio recorded and saved as {filename}")
    return

"""
Sync function
Based on a sync pulse in a given freq, we set the start of each message 
"""
def sync_detect(audiofile, sync_freq):
    fs, audio = read(audiofile)
    # Filter in the frequency
    sos = scipy.signal.butter(5, [sync_freq + 100, sync_freq - 100], "bandpass", fs = fs, output = "sos")
    filtered = scipy.signal.sosfiltfilt(sos, audio)
    # From this we get the peaks
    

    pass

"""
Demodulation function
"""
def demod(audio, freq, fs):
    sos = scipy.signal.butter(5, [freq + 100, freq - 100], "bandpass", fs = fs, output = "sos")
    filtered = scipy.signal.sosfiltfilt(sos, audio)
    pass
"""
Decoding function
"""
def decoder():
    pass
#
# Assembly of functions
def main():
    pass


if __name__ == "__main__":
    print("-------------Receiver Module-------------")
    start = input("Start receiving data? [y/n]: ")
    if (ANS_DIC[start]):
        main()
    else:
         pass
    
