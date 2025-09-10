import numpy as np
import config as cfg
import cv2

def image_ycbcr(R, G, B):
    image = np.array([0, 128, 128])
    
    rgb = np.stack([R, G, B], axis=-1)
    
    ycbcr = np.dot(rgb, cfg.transformation_matrix.T) + image

    Y = ycbcr[:, :, 0]
    Cb = ycbcr[:, :, 1]
    Cr = ycbcr[:, :, 2]
    
    return Y, Cb, Cr

def inv_ycbcr(Y, Cb, Cr): 
    matriz_inversa = np.linalg.inv(cfg.transformation_matrix)

    image = np.stack([Y, Cb - 128, Cr - 128], axis=-1)

    rgb = image @ matriz_inversa.T

    R = rgb[:, :, 0]
    G = rgb[:, :, 1]
    B = rgb[:, :, 2]
    
    R = np.round(R)
    R[R > 255] = 255
    R[R < 0] = 0

    G = np.round(G)
    G[G > 255] = 255
    G[G < 0] = 0

    B = np.round(B)
    B[B > 255] = 255
    B[B < 0] = 0
    
    return R, G, B

def sub_sample(Y, Cb, Cr, cb_v, cr_v, mode):
    if cr_v == 0:
        Cb_d = cv2.resize(Cb, None, fx=(cb_v/4), fy=(cb_v/4), interpolation=mode)
        Cr_d = cv2.resize(Cr, None, fx=(cb_v/4), fy=(cb_v/4), interpolation=mode)
    else:
        Cb_d = cv2.resize(Cb, None, fx=(cb_v/4), fy=1, interpolation=mode)
        Cr_d = cv2.resize(Cr, None, fx=(cr_v/4), fy=1, interpolation=mode)
    
    return Y, Cb_d, Cr_d

def inv_sub_sample(Y, Cb_d, Cr_d, cb_v, cr_v, mode):
    if cr_v == 0:
        Cb = cv2.resize(Cb_d, None, fx=(4/cb_v), fy=(4/cb_v), interpolation=mode)
        Cr = cv2.resize(Cr_d, None, fx=(4/cb_v), fy=(4/cb_v), interpolation=mode)
    else:
        Cb = cv2.resize(Cb_d, None, fx=4/cb_v, fy=1, interpolation=mode)
        Cr = cv2.resize(Cr_d, None, fx=4/cr_v, fy=1, interpolation=mode)
    
    return Y, Cb, Cr
