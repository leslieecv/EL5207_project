import coding as code
import modulation
import soundfile as sf

def transmitter(path,text, f_txt1, f_txt2, f_img_b1, f_img_b2, f_img_g1, f_img_g2, f_img_r1, f_img_r2):
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


    mod_img_0 = modulation.bfsk_modulate(bin_img_0, f_img_b1, f_img_b2, 16, 44100)
    mod_img_1 = modulation.bfsk_modulate(bin_img_1, f_img_g1, f_img_g2, 16, 44100)
    mod_img_2 = modulation.bfsk_modulate(bin_img_2, f_img_r1, f_img_r2, 16, 44100)

    mod_txt = modulation.bfsk_modulate(bin_txt, f_txt1, f_txt2, 16, 44100)

    # Falta agregar el texto
    mod_img = mod_img_0 + mod_img_1 + mod_img_2
    sf.write("mod_img.wav",mod_img, 44100)


# TEST
path = 'data/1_14_Imagen2.png'
text = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 1, primavera 2023.'

f_txt   = [1337, 1883]
f_img_b = [4307, 4803]
f_img_g = [3317, 3813]
f_img_r = [2327, 2823]

transmitter(path,text, f_txt[0], f_txt[1], f_img_b[0], f_img_b[1], f_img_g[0], f_img_g[1], f_img_r[0], f_img_r[1])
