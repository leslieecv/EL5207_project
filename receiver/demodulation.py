"""
Module for the receptor
Made by: Fernanda Borja, Matías Bustos & Leslie Cárdenas
"""
# Import libraries
import decoding as decode
#
import sounddevice as sd
from scipy.io.wavfile import write, read
# Global variables
DURATION = 48 # seconds
SAMPLE_FREQ = 32000 # hertz
ANS_DIC = {"y":1, "n":0}
FREQUENCIES = [[1, 2], [3, 4]] # transmitter [image, text] CHANGE!!!!!!!!!!!

"""
Recording function
Records and stores the data in a .wav file of a given name
"""
def record(seconds: int, fs: int, filename = "output.wav"):
    print(f"Recording with fs = {fs} for {seconds} s...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(f'{filename}', fs, myrecording)
    print("Audio recorded and saved as {filename}")
    return

"""
synchrony detection function
Based on [GIVE PARAMETERS], 
"""
def sync_detect(audiofile, freq_list, n = 2):
    audio = read(audiofile)[1]
    for freqs in freq_list:
        pass
    pass

def demod():
    pass

def decoder():
    pass

def main():
    pass


if __name__ == "__main__":
    print("-------------Receiver Module-------------")
    start = input("Start receiving data? [y/n]: ")
    if (ANS_DIC[start]):
        main()
    else:
         pass
    
