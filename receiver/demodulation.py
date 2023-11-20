"""
Module for the receptor
Made by: Fernanda Borja, Matías Bustos & Leslie Cárdenas
"""
# Import libraries
import decoding as decode
#
import sounddevice as sd
from scipy.io.wavfile import write
# Global variables
DURATION = 48 # seconds
SAMPLE_FREQ = 32000 # hertz
ANS_DIC = {"y":1, "n":0}

def record(seconds, fs, filename = "output.wav"):
    print(f"Recording with fs = {fs} for {seconds} s...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(f'{filename}', fs, myrecording)
    print("Audio recorded and saved as {filename}")
    return
def sync_detect():
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
    
