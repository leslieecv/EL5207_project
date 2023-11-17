import cv2
import numpy as np
import matplotlib.pyplot as plt

def read_image(path):
    img = cv2.imread(path)
    if img is None:
        print("Error: could not read image")
        raise SystemExit
    return img

# cod
def digit_to_bin(digit):
    return '{0:08b}'.format(digit)

def letter_to_bin(letter):
    byte_array = letter.encode()
    binary_int = int.from_bytes(byte_array, "big")
    binary_string = bin(binary_int)
    binary_string = binary_string[2:].zfill(8)
    return binary_string


# decod
def bin_to_letter(binary_string):
    n = int(binary_string, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def bin_to_digit(binary_string):
    return int(binary_string, 2)

#Ejemplo de uso
num_dic= digit_to_bin(8)
ascii_dic = letter_to_bin('A')
r_num = bin_to_digit(num_dic)
r_ascii = bin_to_letter(ascii_dic)
#print(num_dic, r_num, ascii_dic, r_ascii)


def ch_to_bin(ch):
    ch_flatten = ch.flatten()
    func = np.vectorize(digit_to_bin)
    ch_bin = func(ch_flatten)
    vec_bin = ch_bin.flatten()
    return vec_bin

def bin_to_ch(vec_bin):
    n = int(np.sqrt(len(vec_bin)))
    ch_bin = vec_bin.reshape(n, n, 1)
    ch = np.vectorize(bin_to_digit)(ch_bin)
    return ch

# Ejemplo de uso
path = 'data/1_14_Imagen2.png'
img = read_image(path)
img_bin = ch_to_bin(img[:,:,0])
img_dec = bin_to_ch(img_bin)
print(img_dec.shape)
plt.imshow(img_dec, cmap='gray')
plt.show()


