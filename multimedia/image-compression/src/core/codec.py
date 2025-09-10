from quantization.quant import quantization, desquantization
from color_space.ycbcr import image_ycbcr, inv_ycbcr, sub_sample, inv_sub_sample
from utils.utils import padding, despadding
from utils.io import saveImg
from dct.dct_utils import dct_complete, dct_blocks, idct_blocks
from dpcm.dpcm_utils import dpcm_codification, dpcm_descodification

import config as cfg
import numpy as np

def encoder(img, shape, quality, interpolation, output_folder):
    shape = img.shape
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    saveImg(R, output_folder, "red", cfg.cm_red)
    saveImg(G, output_folder,"green", cfg.cm_green)
    saveImg(B, output_folder,"blue", cfg.cm_blue)

    redPad = padding(R, shape[0], shape[1], 32)
    greenPad = padding(G, shape[0], shape[1], 32)
    bluePad = padding(B, shape[0], shape[1], 32)

    saveImg(redPad, output_folder, "red_with_padding", cfg.cm_red)
    saveImg(greenPad, output_folder, "green_with_padding", cfg.cm_green)
    saveImg(bluePad, output_folder, "blue_with_padding", cfg.cm_blue)

    Y, Cb, Cr = image_ycbcr(redPad, greenPad, bluePad)

    saveImg(Y, output_folder, "Y", cfg.cm_gray)
    saveImg(Cb, output_folder, "Cb", cfg.cm_gray)
    saveImg(Cr, output_folder, "Cr", cfg.cm_gray)

    Y_d, Cb_d, Cr_d = sub_sample(Y, Cb, Cr, 2, 2, interpolation)
    
    saveImg(Y_d, output_folder, "Y_d", cfg.cm_gray)
    saveImg(Cb_d, output_folder, "Cb_b", cfg.cm_gray)
    saveImg(Cr_d, output_folder, "Cr_r", cfg.cm_gray)

    Y_dct_c = dct_complete(Y_d)
    Cb_dct_c = dct_complete(Cb_d)
    Cr_dct_c = dct_complete(Cr_d)

    saveImg(np.log(np.abs(Y_dct_c) + 0.0001), output_folder, "Y_DCT", cfg.cm_gray)
    saveImg(np.log(np.abs(Cb_dct_c) + 0.0001), output_folder, "Cb_DCT", cfg.cm_gray)
    saveImg(np.log(np.abs(Cr_dct_c) + 0.0001), output_folder, "Cr_DCT", cfg.cm_gray)

    Y_dct = dct_blocks(Y_d, 8)
    Cb_dct = dct_blocks(Cb_d, 8)
    Cr_dct = dct_blocks(Cr_d, 8)

    saveImg(np.log(np.abs(Y_dct) + 0.0001), output_folder, "Yb_DCT", cfg.cm_gray)
    saveImg(np.log(np.abs(Cb_dct) + 0.0001), output_folder, "Cbb_DCT", cfg.cm_gray)
    saveImg(np.log(np.abs(Cr_dct) + 0.0001), output_folder, "Crb_DCT", cfg.cm_gray)

    Y_quantized, Cb_quantized, Cr_quantized = quantization(Y_dct, Cb_dct, Cr_dct, quality, 8, output_folder)
    Y_quantized[Y_quantized == -0] = 0
    
    Y_dpcm, Cb_dpcm, Cr_dpcm = dpcm_codification(Y_quantized, Cb_quantized, Cr_quantized, 8, output_folder)

    return Y_dpcm, Cb_dpcm, Cr_dpcm, Y

def decoder(Y, Cb, Cr, shape, quality, interpolation, output_folder):
    iDc = dpcm_descodification(Y, 8), dpcm_descodification(Cb, 8), dpcm_descodification(Cr, 8)

    saveImg(np.log(np.abs(iDc[0]) + 0.0001), output_folder,"Yb_iDPCM", cfg.cm_gray)
    saveImg(np.log(np.abs(iDc[1]) + 0.0001), output_folder,"Cbb_iDPCM", cfg.cm_gray)
    saveImg(np.log(np.abs(iDc[2]) + 0.0001), output_folder,"Crb_iDPCM", cfg.cm_gray)

    Y_dct, Cb_dct, Cr_dct = desquantization(iDc[0], iDc[1], iDc[2], quality, 8)

    Y_idct = idct_blocks(Y_dct, 8)
    Cb_idct = idct_blocks(Cb_dct, 8)
    Cr_idct = idct_blocks(Cr_dct, 8)
    Y, Cb, Cr = inv_sub_sample(Y_idct, Cb_idct, Cr_idct, 2, 2, interpolation)

    
    redPad, greenPad, bluePad = inv_ycbcr(Y, Cb, Cr)

    imgRec = np.zeros((shape[0], shape[1], 3), dtype = np.uint8)

    R = despadding(redPad, shape[0], shape[1])
    G = despadding(greenPad, shape[0], shape[1])
    B = despadding(bluePad, shape[0], shape[1])

    imgRec[:, :, 0] = R
    imgRec[:, :, 1] = G
    imgRec[:, :, 2] = B

    return imgRec, Y
