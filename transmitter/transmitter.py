import coding as code
import modulation
import soundfile as sf
import numpy as np
from scipy import signal

def str_to_int(arrays):
    int_array = []
    for array in arrays:
        int_array.append([int(char) for char in array])
    if len(int_array)==1:
        return int_array[0]
    return int_array

def transmitter(path, text, SYNC_FREQ, FREQUENCIES, BAUD = 40, SAMPLE_FREQ= 44100):
    cod_img = code.Coding(path, mode='image')
    cod_chs = str_to_int(cod_img.data_bin)

    cod_txt = code.Coding(text, mode='text')
    cod_txt = str_to_int([cod_txt.data_bin])

    mod_img = []
    for i in range(1, len(FREQUENCIES)):
        ch_mod = modulation.bfsk_modulate(cod_chs[i-1], FREQUENCIES[i][0], FREQUENCIES[i][1], BAUD, SAMPLE_FREQ)
        mod_img.append(ch_mod)
        print(len(ch_mod))
    mod_img_sum = np.sum(np.array(mod_img), axis = 0)
    print(len(mod_img_sum))
    mod_txt = modulation.bfsk_modulate(cod_txt, FREQUENCIES[0][0], FREQUENCIES[0][1], BAUD, SAMPLE_FREQ)
    
    points = np.linspace(0, 1, int(SAMPLE_FREQ*1))
    sync_mod_init = signal.chirp(points, SYNC_FREQ[0], 1, np.mean(SYNC_FREQ))
    sync_mod_end  = signal.chirp(points, SYNC_FREQ[1], 1, np.mean(SYNC_FREQ))
    print(len(sync_mod_init), len(sync_mod_end))
    mod_trans = np.concatenate([sync_mod_init, mod_img_sum, sync_mod_end, sync_mod_init, mod_txt, sync_mod_end], axis=None)
    print(len(mod_trans))
    return mod_trans
    #sf.write("mod_img_sync.wav",mod_img, 44100)

# TEST
path1 = 'data/1_20_Imagen1.png'
text1 = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 1, primavera 2023. '

path2 = 'data/1_14_Imagen2.png'
text2 = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 2, primavera 2023. '
paths = [path1, path2]
texts = [text1, text2]

# Global variables
BAUD = 40
DURATION = 120 # seconds
SAMPLE_FREQ = 44100 # hertz
SYNC_FREQ = [[348, 894], [5298, 5792]]
FREQUENCIES = [
    [[1337, 3317],  # Text
     [1883, 3813],  # R
     [2327, 4307],  # G
     [2823, 4803]], # B
    [[6287, 8267],  # Text
     [6783, 8763],  # R
     [7277, 9257],  # G
     [7773, 9753],]]# B

mod_trans = []
for i in range(len(FREQUENCIES)):
    print('Modulation trans')
    mod_em= transmitter(paths[i], texts[i], SYNC_FREQ[i], FREQUENCIES[i], BAUD, SAMPLE_FREQ)
    mod_trans.append(mod_em)
    sf.write(f"tests//test{i}.wav",mod_em, 44100)

while len(mod_trans[0]) < len(mod_trans[1]):
    mod_trans[0].append(0)
while len(mod_trans[1]) < len(mod_trans[0]):
    mod_trans[1].append(0)

print(len(mod_trans[0]), len(mod_trans[1]))

print(np.max([len(mod_trans[0]), len(mod_trans[1])]))

n_max = np.max([len(mod_trans[0]), len(mod_trans[1])])

mod_img = np.sum(np.array(mod_trans), axis = 0)
print(len(mod_img))
sf.write("tests//test3.wav",mod_img, 44100)

