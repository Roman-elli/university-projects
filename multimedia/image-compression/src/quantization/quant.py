import numpy as np
import config as cfg

from utils.io import saveImg

def quantization(q_Y, q_Cb, q_Cr, quality, bloco, output_folder):
    if(quality >= 50):
        Sf = (100 - quality) / 50
    else:
        Sf = 50 / quality
    
    if(Sf != 0):
        quant_Y_quality = np.round(cfg.quant_Y * Sf)
        quant_CbCr_quality = np.round(cfg.quant_CbCr * Sf)
    else:
        quant_Y_quality = cfg.all_one
        quant_CbCr_quality = cfg.all_one

    quant_Y_quality = np.clip(quant_Y_quality, 1, 255)
    quant_CbCr_quality = np.clip(quant_CbCr_quality, 1, 255)

    line, column = q_Y.shape
    line_CbCr, column_CbCr = q_Cb.shape

    q_Y_result = np.zeros((line, column))
    q_Cb_result = np.zeros((line_CbCr, column_CbCr))
    q_Cr_result = np.zeros((line_CbCr, column_CbCr))

    for i in range(0, line, bloco):
        for j in range(0, column, bloco):
            q_Y_result[i:i+bloco, j:j+bloco] = np.round(q_Y[i:i+bloco, j:j+bloco] / quant_Y_quality)

    for i in range(0, line_CbCr, bloco):
        for j in range(0, column_CbCr, bloco):
            q_Cb_result[i:i+bloco, j:j+bloco] = np.round(q_Cb[i:i+bloco, j:j+bloco] / quant_CbCr_quality)
            q_Cr_result[i:i+bloco, j:j+bloco] = np.round(q_Cr[i:i+bloco, j:j+bloco] / quant_CbCr_quality)

    saveImg(np.log(np.abs(q_Y_result) + 0.0001), output_folder, f"Y_Quantized {quality}", cfg.cm_gray)
    saveImg(np.log(np.abs(q_Cb_result) + 0.0001), output_folder, f"Cb_Quantized {quality}", cfg.cm_gray)
    saveImg(np.log(np.abs(q_Cr_result) + 0.0001), output_folder, f"Cr_Quantized {quality}", cfg.cm_gray)

    return q_Y_result, q_Cb_result, q_Cr_result

def desquantization(q_Y, q_Cb, q_Cr, quality, bloco):
    if(quality >= 50):
        Sf = (100 - quality) / 50
    else:
        Sf = 50 / quality
    
    if(Sf != 0):
        quant_Y_quality = np.round(cfg.quant_Y * Sf)
        quant_CbCr_quality = np.round(cfg.quant_CbCr * Sf)
    else:
        quant_Y_quality = cfg.all_one
        quant_CbCr_quality = cfg.all_one

    quant_Y_quality = np.clip(quant_Y_quality, 1, 255)
    quant_CbCr_quality = np.clip(quant_CbCr_quality, 1, 255)

    line, column = q_Y.shape
    line_CbCr, column_CbCr = q_Cb.shape

    q_Y_result = np.zeros((line, column))
    q_Cb_result = np.zeros((line_CbCr, column_CbCr))
    q_Cr_result = np.zeros((line_CbCr, column_CbCr))

    for i in range(0, line, bloco):
        for j in range(0, column, bloco):
            q_Y_result[i:i+bloco, j:j+bloco] = q_Y[i:i+bloco, j:j+bloco] * quant_Y_quality

    for i in range(0, line_CbCr, bloco):
        for j in range(0, column_CbCr, bloco):
            q_Cb_result[i:i+bloco, j:j+bloco] = q_Cb[i:i+bloco, j:j+bloco] * quant_CbCr_quality
            q_Cr_result[i:i+bloco, j:j+bloco] = q_Cr[i:i+bloco, j:j+bloco] * quant_CbCr_quality

    return q_Y_result, q_Cb_result, q_Cr_result
