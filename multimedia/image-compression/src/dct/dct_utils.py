from scipy.fftpack import dct, idct
import numpy as np

def dct_complete(channel):
    return dct(dct(channel, norm='ortho').T, norm='ortho').T

def idct_complete(channel_dct):
    return idct(idct(channel_dct, norm="ortho").T, norm="ortho").T

def dct_blocks(channel, BS):
    h, w = channel.shape
    dct_result = np.zeros((h, w))
    
    for i in range(0, h, BS):
        for j in range(0, w, BS):
            block = channel[i:i+BS, j:j+BS]
            dct_result[i:i+BS, j:j+BS] = dct_complete(block)
    
    return dct_result

def idct_blocks(channel_dct, BS):
    h, w = channel_dct.shape
    idct_result = np.zeros((h, w))
    
    for i in range(0, h, BS):
        for j in range(0, w, BS):
            block = channel_dct[i:i+BS, j:j+BS]
            idct_result[i:i+BS, j:j+BS] = idct_complete(block)
    
    return idct_result
