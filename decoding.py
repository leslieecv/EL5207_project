import cv2
import numpy as np
import matplotlib.pyplot as plt

from coding import Coding
class Decoding:
    def __init__(self, src, mode):
        self.data = src
        if mode == 'text':
            self.split_bin(self.data)
            bin_vec = self.text_to_bin(src)
            self.decod_data = bin_vec[0]

        elif mode == 'image':
            self.decod_data = []
            for bin_ch in src:
                bin_vec = self.split_bin(bin_ch)                
                decod_ch = self.bin_to_ch(bin_vec)
                self.decod_data.append(decod_ch)
            self.decod_data = cv2.merge(self.decod_data)
            
    def split_bin(self, bin_ch):
        assert len(bin_ch) % 8 == 0, "Error: data must be multiple of 8"
        return [bin_ch[i:i+8] for i in range(0, len(bin_ch), 8)]

    # decod
    def bin_to_letter(self, binary_string):
        n = int(binary_string, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    
    def text_to_bin(self, text):
        func = np.vectorize(self.bin_to_letter)
        text_bin = func(text)
        vec_bin = text_bin.flatten()
        return vec_bin

    def bin_to_digit(self, binary_string):
        return int(binary_string, 2)

    def bin_to_ch(self, vec_bin):
        n = int(np.sqrt(len(vec_bin)))
        vec_bin = np.array(vec_bin)
        ch_bin = vec_bin.reshape(n, n)
        ch = np.vectorize(self.bin_to_digit)(ch_bin)
        return ch


def main():
    text1 = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 1, primavera 2023.'
    cod = Coding(text1, mode='text')
    cod_ch = cod.data_bin
    decod = Decoding(cod_ch, mode='text')
    decod_ch = decod.decod_data

    print('------ imagen -------')
    path = 'data/1_14_Imagen2.png'
    cod = Coding(path, mode='image')
    cod_ch = cod.data_bin
    decod = Decoding(cod_ch, mode='image')
    decod_ch = decod.decod_data
    plt.imshow(decod_ch, cmap='gray')
    plt.show()

if __name__ == "__main__":
    main()