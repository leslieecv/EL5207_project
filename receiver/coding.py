import cv2
import numpy as np
import matplotlib.pyplot as plt

class Coding:
    def __init__(self, src, mode):
        if mode == 'text':
            self.data = src
            bin_vec = self.text_to_bin(self.data)
            self.data_bin = self.join_bin(bin_vec)
        elif mode == 'image':
            self.data = self.read_image(src)
            self.data_bin = []
            for ch in self.data:
                bin_ch = self.ch_to_bin(ch)
                bin_vec = self.join_bin(bin_ch)
                self.data_bin.append(bin_vec)
                
    def read_image(self, path):
        img = cv2.imread(path)
        if img is None:
            print("Error: could not read image")
            raise SystemExit
        chB, chG, chR = cv2.split(img)
        return [chR, chG, chB]
    
    def join_bin(self, bin_ch):
        return ''.join(bin_ch)

    # For image
    def ch_to_bin(self, ch):
        ch_flatten = ch.flatten()
        func = np.vectorize(self.digit_to_bin)
        ch_bin = func(ch_flatten)
        vec_bin = ch_bin.flatten()
        return vec_bin
    
    def digit_to_bin(self, digit):
        return '{0:08b}'.format(digit)
    
    # For text
    def text_to_bin(self, text):
        func = np.vectorize(self.letter_to_bin)
        text_bin = func(text)
        vec_bin = text_bin.flatten()
        return vec_bin
    
    def letter_to_bin(self, letter):
        byte_array = letter.encode()
        binary_int = int.from_bytes(byte_array, "big")
        binary_string = bin(binary_int)
        binary_string = binary_string[2:].zfill(8)
        return binary_string
    
def main():
    # En el emisor:
    print('------ imagen -------')
    path = 'data/1_14_Imagen2.png'
    cod = Coding(path, mode='image')
    cod_ch = cod.data_bin[0]
    print(cod_ch)

    print('------ texto -------')

    text1 = '¡Laboratorio  de  Tecnologías  de  Información  y  de  Comunicación EL5207! Transmisor número 1, primavera 2023.'
    cod = Coding(text1, mode='text')
    cod_ch = cod.data_bin
    print(cod_ch)

if __name__ == "__main__":
    main()



