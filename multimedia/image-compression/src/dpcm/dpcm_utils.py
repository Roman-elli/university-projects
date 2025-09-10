import numpy as np
import config as cfg

from utils.io import saveImg


def dpcm_codification(Y_q, Cb_q, Cr_q, jump, output_folder):
    line, column = Y_q.shape
    line_CbCr, column_CbCr = Cb_q.shape

    Y_dpcm = np.zeros((line, column))
    Cb_dpcm = np.zeros((line_CbCr, column_CbCr))
    Cr_dpcm = np.zeros((line_CbCr, column_CbCr))
    
    for i in range(0, line, jump):
        for j in range(0, column, jump):
            if (j == 0 and i == 0):
                Y_dpcm[i, j] = Y_q[i, j]
            elif (j == 0):
                Y_dpcm[i, j] = Y_q[i, j] - Y_q[i-jump, range(0, column, jump)[-1]]
            else:
                Y_dpcm[i, j] = Y_q[i, j] - Y_q[i, j-jump]
                
    for i in range(0, line_CbCr, jump):
        for j in range(0, column_CbCr, jump):
            if (j == 0 and i == 0):
                Cb_dpcm[i, j] = Cb_q[i, j]
                Cr_dpcm[i, j] = Cr_q[i, j]
            elif (j == 0):
                Cb_dpcm[i, j] = Cb_q[i, j] - Cb_q[i-jump, range(0, column_CbCr, jump)[-1]]
                Cr_dpcm[i, j] = Cr_q[i, j] - Cr_q[i-jump, range(0, column_CbCr, jump)[-1]]
            else:
                Cb_dpcm[i, j] = Cb_q[i, j] - Cb_q[i, j-jump]
                Cr_dpcm[i, j] = Cr_q[i, j] - Cr_q[i, j-jump]
    
    for i in range(0, line, jump):
        for j in range(0, column, jump):
            Y_q[i, j] = Y_dpcm[i, j]
    
    for i in range(0, line_CbCr, jump):
        for j in range(0, column_CbCr, jump):
            Cb_q[i, j] = Cb_dpcm[i, j]
            Cr_q[i, j] = Cr_dpcm[i, j]
    
    saveImg(np.log(np.abs(Y_q) + 0.0001), output_folder, "Y_dpcm_log_abs", cfg.cm_gray)
    saveImg(np.log(np.abs(Cb_q) + 0.0001), output_folder, "Cb_dpcm_log_abs", cfg.cm_gray)
    saveImg(np.log(np.abs(Cr_q) + 0.0001), output_folder, "Cr_dpcm_log_abs", cfg.cm_gray)
    saveImg(Y_q, output_folder, "Y_dpcm", cfg.cm_gray)
    saveImg(Cb_q, output_folder, "Cb_dpcm", cfg.cm_gray)
    saveImg(Cr_q, output_folder, "Cr_dpcm", cfg.cm_gray)
    
    return Y_q, Cb_q, Cr_q

def dpcm_descodification(channel, block):
    dc = channel.copy()

    for i in range(0, len(channel), block):
        for j in range(0, len(channel[0]), block):
            if j == 0:
                if i != 0:
                    dc[i][j] = dc[i - block][len(channel[0])-block] + channel[i][j]
            else:
                dc[i][j] = dc[i][j-block] + channel[i][j]

    return dc
