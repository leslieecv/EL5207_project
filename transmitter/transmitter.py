import coding as code
import modulation
import soundfile as sf
import numpy as np
from scipy import signal

def transmitter(path,text,baud, f_sync1, f_sync2, f_txt1, f_txt2, f_img_b1, f_img_b2, f_img_g1, f_img_g2, f_img_r1, f_img_r2):
    cod_img = code.Coding(path, mode='image')
    bin_img_0 = [*cod_img.data_bin[0]]
    bin_img_0 = [eval(i) for i in bin_img_0]

    bin_img_1 = [*cod_img.data_bin[1]]
    bin_img_1 = [eval(i) for i in bin_img_1]

    bin_img_2 = [*cod_img.data_bin[2]]
    bin_img_2 = [eval(i) for i in bin_img_2]

    
    cod_txt = code.Coding(text, mode='text')
    bin_txt = [*cod_txt.data_bin]
    bin_txt = [eval(i) for i in bin_txt]

    sync = [1,1,1,1]
    sync2 = [0,0,0,0]
    #noise = [0,1,1,1,1,0,0,1,0,0,1]


    #noise_mod = modulation.bfsk_modulate(noise, 400, 600, baud, 44100)
    # sync_mod_init = modulation.bfsk_modulate(sync, f_sync1, f_sync2, baud, 44100)
    # sync_mod_end  = modulation.bfsk_modulate(sync2, f_sync1, f_sync2, baud, 44100)
    points = np.linspace(0, 1, int(44100*1))
    sync_mod_init = signal.chirp(points, f_sync1, 1, np.mean([f_sync1, f_sync2]))
    sync_mod_end  = signal.chirp(points, f_sync2, 1, np.mean([f_sync1, f_sync2]))
    mod_img_0 = modulation.bfsk_modulate(bin_img_0, f_img_b1, f_img_b2, baud, 44100)
    mod_img_1 = modulation.bfsk_modulate(bin_img_1, f_img_g1, f_img_g2, baud, 44100)
    mod_img_2 = modulation.bfsk_modulate(bin_img_2, f_img_r1, f_img_r2, baud, 44100)

    mod_txt = modulation.bfsk_modulate(bin_txt, f_txt1, f_txt2, baud, 44100)

    # Falta agregar el texto
    mod_img = mod_img_0 + mod_img_1 + mod_img_2

    #agregar sync_mod al inicio y al final
    #return np.concatenate((sync_mod, mod_img, sync_mod), axis=None)
    print("listoco")
    mod_img = np.concatenate((sync_mod_init, mod_img, sync_mod_end, sync_mod_init, mod_txt, sync_mod_end), axis=None)
    return mod_img
    #sf.write("mod_img_sync.wav",mod_img, 44100)


# TEST
path1 = 'data/1_20_Imagen1.png'
text1 = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 1, primavera 2023. '

path2 = 'data/1_14_Imagen2.png'
text2 = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 2, primavera 2023. '

baud = 40

f_sync_1  = [348, 894]
f_txt_1   = [1337, 1883]
f_img_b_1 = [4307, 4803]
f_img_g_1 = [3317, 3813]
f_img_r_1 = [2327, 2823]

f_sync_2  = [5298, 5792]
f_txt_2   = [6287, 6783]
f_img_b_2 = [7277, 7773]
f_img_g_2 = [8267, 8763]
f_img_r_2 = [9257, 9753]


imagen1= transmitter(path1,text1, baud, f_sync_1[0], f_sync_1[1], f_txt_1[0], f_txt_1[1], f_img_b_1[0], f_img_b_1[1], f_img_g_1[0], f_img_g_1[1], f_img_r_1[0], f_img_r_1[1])
imagen2= transmitter(path2,text2, baud, f_sync_2[0], f_sync_2[1], f_txt_2[0], f_txt_2[1], f_img_b_2[0], f_img_b_2[1], f_img_g_2[0], f_img_g_2[1], f_img_r_2[0], f_img_r_2[1])


#sumar los 2 audios 
n_max = max(len(imagen1),len(imagen2))

#agregar 0 al vector de menor tamaño
if len(imagen1) < n_max:
    imagen1 = np.concatenate((imagen1, np.zeros(n_max-len(imagen1))), axis=None)
if len(imagen2) < n_max:
    imagen2 = np.concatenate((imagen2, np.zeros(n_max-len(imagen2))), axis=None)

mod_img = imagen1 + imagen2
sf.write("tests//test3.wav",mod_img, 44100)

