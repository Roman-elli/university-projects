import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import cv2
from scipy.fftpack import dct, idct

cm_red = clr.LinearSegmentedColormap.from_list("red", [(0, 0, 0), (1, 0, 0)], N = 256)
cm_green = clr.LinearSegmentedColormap.from_list("green", [(0, 0, 0), (0, 1, 0)], N = 256)
cm_blue = clr.LinearSegmentedColormap.from_list("blue", [(0, 0, 0), (0, 0, 1)], N = 256)
cm_gray = clr.LinearSegmentedColormap.from_list("gray", [(0, 0, 0), (1, 1, 1)], N = 256)

# Matriz de conversão RGB para YCbCr
transformation_matriz = np.array([[0.299, 0.587, 0.114],
                                  [-0.168736, -0.331264, 0.5],
                                  [0.5, -0.418688, -0.081312]])

quant_Y = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

quant_CbCr = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]
])

all_one = np.ones((8, 8), dtype=np.float32)

#-------------------------------------------------------------------------------------------
def showImg(img, title, cmap = None):
    plt.figure()
    plt.imshow(img, cmap)
    plt.axis("off")
    plt.title(title)
    plt.show()

#-------------------------------------------------------------------------------------------
def showSubMatriz(img, l, c, dim):
    nd = img.ndim
    if nd == 2:
        print(np.round(img[l:l+dim, c:c+dim], 3))
    elif nd == 3:
        print(np.round(img[l:l+dim, c:c+dim, 0], 3))

# EXERCÍCIO 4 -------------------------------------------------------------------------------------------
def padding(matriz, nl, nc, dim):
    # Numero de linha a adicionar
    addLine = dim - (nl % dim)

    # Numero de colunas a adicionar
    addColumn = dim - (nc % dim)

    # Criar padding de linhas com base na última linha
    ultima_linha = matriz[-1, :]
    matrizLine = np.tile(ultima_linha, (addLine, 1))
    matriz = np.vstack((matriz, matrizLine))

    # Criar padding de colunas com base na última coluna
    ultima_coluna = matriz[:, -1]
    matrizColumn = np.tile(ultima_coluna[:, None], (1, addColumn))
    matriz = np.hstack((matriz, matrizColumn))
    return matriz

#-------------------------------------------------------------------------------------------
def despadding(matriz, nl, nc):
    return matriz[:nl, :nc]

# EXERCÍCIO 5 -------------------------------------------------------------------------------------------
def image_ycbcr(R, G, B):
    # Vetor adicional (offset)
    image = np.array([0, 128, 128])
    
    #transforma R G B matrizes(2D) (altura, largura) numa 3D (altura, largura, 3)
    rgb = np.stack([R, G, B], axis=-1)
    
    # Cálculo do Y, Cb e Cr
    ycbcr = np.dot(rgb, transformation_matriz.T) + image

    Y = ycbcr[:, :, 0]
    Cb = ycbcr[:, :, 1]
    Cr = ycbcr[:, :, 2]
    
    return Y, Cb, Cr

#-------------------------------------------------------------------------------------------
def inv_ycbcr(Y, Cb, Cr): 
    matriz_inversa = np.linalg.inv(transformation_matriz)

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

# EXERCÍCIO 6 -------------------------------------------------------------------------------------------
def sub_sample(Y, Cb, Cr, cb_v, cr_v, mode):
    if cr_v == 0:
        Cb_d = cv2.resize(Cb, None, fx=(cb_v/4), fy=(cb_v/4), interpolation=mode)
        Cr_d = cv2.resize(Cr, None, fx=(cb_v/4), fy=(cb_v/4), interpolation=mode)
    else:
        # cr_v != 0
        Cb_d = cv2.resize(Cb, None, fx=(cb_v/4), fy=1, interpolation=mode)
        Cr_d = cv2.resize(Cr, None, fx=(cr_v/4), fy=1, interpolation=mode)
    

    # print(Cb.shape)
    # print(Cb_d.shape)

    return Y, Cb_d, Cr_d

#-------------------------------------------------------------------------------------------
def inv_sub_sample(Y, Cb_d, Cr_d, cb_v, cr_v, mode):
    if cr_v == 0:
        Cb = cv2.resize(Cb_d, None, fx=(4/cb_v), fy=(4/cb_v), interpolation=mode)
        Cr = cv2.resize(Cr_d, None, fx=(4/cb_v), fy=(4/cb_v), interpolation=mode)
    else:
        # cr_v != 0
        Cb = cv2.resize(Cb_d, None, fx=4/cb_v, fy=1, interpolation=mode)
        Cr = cv2.resize(Cr_d, None, fx=4/cr_v, fy=1, interpolation=mode)
    
    # print(Cb.shape)
    # print(Cb_d.shape)
    return Y, Cb, Cr

# EXERCÍCIO 7 -------------------------------------------------------------------------------------------
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

# EXERCÍCIO 8 -------------------------------------------------------------------------------------------
def quantization(q_Y, q_Cb, q_Cr, quality, bloco):
    # Calculo fator de qualidade
    if(quality >= 50):
        Sf = (100 - quality) / 50
    else:
        Sf = 50 / quality
    
    if(Sf != 0):
        quant_Y_quality = np.round(quant_Y * Sf)
        quant_CbCr_quality = np.round(quant_CbCr * Sf)
    else:
        quant_Y_quality = all_one
        quant_CbCr_quality = all_one

    print("==================================================================================")
    print("EXERCICIO 8 - QY")
    print(quant_Y_quality)

    # Garantindo que os valores fiquem entre 1 e 255
    quant_Y_quality = np.clip(quant_Y_quality, 1, 255)
    quant_CbCr_quality = np.clip(quant_CbCr_quality, 1, 255)

    # Aplica o calculo de Quantização nos tres canais
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

    # Apresentar resultados
    showImg(np.log(np.abs(q_Y_result) + 0.0001), f"Y_Quantized {quality}", cm_gray)
    showImg(np.log(np.abs(q_Cb_result) + 0.0001), f"Cb_Quantized {quality}", cm_gray)
    showImg(np.log(np.abs(q_Cr_result) + 0.0001), f"Cr_Quantized {quality}", cm_gray)

    

    return q_Y_result, q_Cb_result, q_Cr_result

#-------------------------------------------------------------------------------------------
def desquantization(q_Y, q_Cb, q_Cr, quality, bloco):
    # Calculo fator de qualidade
    if(quality >= 50):
        Sf = (100 - quality) / 50
    else:
        Sf = 50 / quality
    
    if(Sf != 0):
        quant_Y_quality = np.round(quant_Y * Sf)
        quant_CbCr_quality = np.round(quant_CbCr * Sf)
    else:
        quant_Y_quality = all_one
        quant_CbCr_quality = all_one
    
    print("==================================================================================")
    print("EXERCICIO 8 - QY")
    print(quant_Y_quality)

    # Garantindo que os valores fiquem entre 1 e 255
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

# EXERCÍCIO 9 -------------------------------------------------------------------------------------------
def dpcm_codification(Y_q, Cb_q, Cr_q, jump):
    line, column = Y_q.shape
    line_CbCr, column_CbCr = Cb_q.shape

    Y_dpcm = np.zeros((line, column))
    Cb_dpcm = np.zeros((line_CbCr, column_CbCr))
    Cr_dpcm = np.zeros((line_CbCr, column_CbCr))
    
    # print("Pre dpcm:")
    # showSubMatriz(Y_q, 8, 8, 8)
    # showSubMatriz(Cb_q, 8, 8, 8)
    # showSubMatriz(Cr_q, 8, 8, 8)
    
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
    
    # print("Pos dpcm:")
    # showSubMatriz(Y_q, 8, 8, 8)
    # showSubMatriz(Cb_q, 8, 8, 8)
    # showSubMatriz(Cr_q, 8, 8, 8)

    # Apresentar resultados
    showImg(np.log(np.abs(Y_q) + 0.0001), "Y_dpcm", cm_gray)
    showImg(np.log(np.abs(Cb_q) + 0.0001), "Cb_dpcm", cm_gray)
    showImg(np.log(np.abs(Cr_q) + 0.0001), "Cr_dpcm", cm_gray)
    showImg(Y_q, "Y_dpcm", cm_gray)
    showImg(Cb_q, "Cb_dpcm", cm_gray)
    showImg(Cr_q, "Cr_dpcm", cm_gray)
    
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

# EXERCÍCIO 10 -------------------------------------------------------------------------------------------
def diff_Y(Yo, Yr, img, imgRec, quality):
    diff = np.abs(Yo - Yr)

    diff = (diff / np.max(diff)) * 255 if np.max(diff) > 0 else diff
    diff = diff.astype(np.uint8)

    showImg(diff, "Imagem diferenças", cm_gray)

    img = img.astype(np.uint16)

    mse = np.sum((img - imgRec) ** 2) / (img.shape[0] * img.shape[1])

    rmse = np.sqrt(mse)

    P = np.sum(img**2) / (img.shape[0] * img.shape[1])

    snr = 10*np.log10(P/mse)

    psnr = 10*np.log10((np.max(img)) **2/mse)

    print("==================================================================================")
    print("EXERCICIO 10 -> qualidade ", quality)
    print("Max Diff: ", np.max(diff))
    print("Avg Diff: ", np.mean(diff))
    print("MSE: ", mse)
    print("RMSE: ", rmse)
    print("SNR: ", snr)
    print("PSNR: ", psnr)

#-------------------------------------------------------------------------------------------
def encoder(img, shape, quality, interpolation):
    shape = img.shape
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    showImg(R, "Red", cm_red)
    showImg(G, "Green", cm_green)
    showImg(B, "Blue", cm_blue)

    print("EXERCICIO 3 - channel R")
    showSubMatriz(R, 8, 8, 8)

    # EXERCICIO 4
    redPad = padding(R, shape[0], shape[1], 32)
    greenPad = padding(G, shape[0], shape[1], 32)
    bluePad = padding(B, shape[0], shape[1], 32)

    showImg(redPad, "Red com Padding", cm_red)
    showImg(greenPad, "Green com Padding", cm_green)
    showImg(bluePad, "Blue com Padding", cm_blue)

    # EXERCICIO 5
    Y, Cb, Cr = image_ycbcr(redPad, greenPad, bluePad)

    showImg(Y, "Y", cm_gray)
    showImg(Cb, "Cb", cm_gray)
    showImg(Cr, "Cr", cm_gray)

    print("==================================================================================")
    print("EXERCICIO 5 - Y")
    showSubMatriz(Y, 8, 8, 8)
    print("----------------------------------------------------------------------------------")
    print("EXERCICIO 5 - Cb")
    showSubMatriz(Cb, 8, 8, 8)

    # EXERCICIO 6
    Y_d, Cb_d, Cr_d = sub_sample(Y, Cb, Cr, 2, 2, interpolation)
    
    showImg(Y_d, "Y_d", cm_gray)
    showImg(Cb_d, "Cb_b", cm_gray)
    showImg(Cr_d, "Cr_r", cm_gray)

    print("==================================================================================")
    print("EXERCICIO 6 - Cb")
    showSubMatriz(Cb, 8, 8, 8)

    # EXERCICIO 7
    #mostra os resultados da página 5
    Y_dct_c = dct_complete(Y_d)
    Cb_dct_c = dct_complete(Cb_d)
    Cr_dct_c = dct_complete(Cr_d)
    showImg(np.log(np.abs(Y_dct_c) + 0.0001), "Y_DCT", cm_gray)
    showImg(np.log(np.abs(Cb_dct_c) + 0.0001), "Cb_DCT", cm_gray)
    showImg(np.log(np.abs(Cr_dct_c) + 0.0001), "Cr_DCT", cm_gray)

    # mostra os resultados da página 6
    Y_dct = dct_blocks(Y_d, 8)
    Cb_dct = dct_blocks(Cb_d, 8)
    Cr_dct = dct_blocks(Cr_d, 8)

    print("==================================================================================")
    print("EXERCICIO 7 - Yb_dct")
    showSubMatriz(Y_dct, 8, 8, 8)

    showImg(np.log(np.abs(Y_dct) + 0.0001), "Yb_DCT", cm_gray)
    showImg(np.log(np.abs(Cb_dct) + 0.0001), "Cbb_DCT", cm_gray)
    showImg(np.log(np.abs(Cr_dct) + 0.0001), "Crb_DCT", cm_gray)

    # EXERCICIO 8
    Y_quantized, Cb_quantized, Cr_quantized = quantization(Y_dct, Cb_dct, Cr_dct, quality, 8)

    print("----------------------------------------------------------------------------------")
    print("EXERCICIO 8 - Yb_quantized")
    Y_quantized[Y_quantized == -0] = 0
    showSubMatriz(Y_quantized, 8, 8, 8)
    
    # EXERCICIO 9
    Y_dpcm, Cb_dpcm, Cr_dpcm = dpcm_codification(Y_quantized, Cb_quantized, Cr_quantized, 8)

    print("==================================================================================")
    print("EXERCICIO 9 - Yb_dpcm")
    showSubMatriz(Y_dpcm, 8, 8, 8)

    return Y_dpcm, Cb_dpcm, Cr_dpcm, Y

#-------------------------------------------------------------------------------------------
def decoder(Y, Cb, Cr, shape, quality, interpolation):
    print("==================================================================================")
    print("=======================================DECODER====================================")
    # EXERCICIO 9
    iDc = dpcm_descodification(Y, 8), dpcm_descodification(Cb, 8), dpcm_descodification(Cr, 8)

    #resultado exercício 9
    showImg(np.log(np.abs(iDc[0]) + 0.0001), "Yb_iDPCM", cm_gray)
    showImg(np.log(np.abs(iDc[1]) + 0.0001), "Cbb_iDPCM", cm_gray)
    showImg(np.log(np.abs(iDc[2]) + 0.0001), "Crb_iDPCM", cm_gray)

    print("==================================================================================")
    print("EXERCICIO 9 - Yb_dpcm")
    showSubMatriz(iDc[0], 8, 8, 8)

    Y_dct, Cb_dct, Cr_dct = desquantization(iDc[0], iDc[1], iDc[2], quality, 8)

    print("----------------------------------------------------------------------------------")    
    print("EXERCICIO 8 - Yb_quantized")
    showSubMatriz(Y_dct, 8, 8, 8)

    Y_idct = idct_blocks(Y_dct, 8)
    Cb_idct = idct_blocks(Cb_dct, 8)
    Cr_idct = idct_blocks(Cr_dct, 8)

    print("==================================================================================")
    print("EXERCICIO 7 - Yb_dct")
    showSubMatriz(Y_idct, 8, 8, 8)

    Y, Cb, Cr = inv_sub_sample(Y_idct, Cb_idct, Cr_idct, 2, 2, interpolation)

    print("==================================================================================")
    print("EXERCICIO 6 - Cb")
    showSubMatriz(Cb, 8, 8, 8)
    
    redPad, greenPad, bluePad = inv_ycbcr(Y, Cb, Cr)

    imgRec = np.zeros((shape[0], shape[1], 3), dtype = np.uint8)

    R = despadding(redPad, shape[0], shape[1])
    G = despadding(greenPad, shape[0], shape[1])
    B = despadding(bluePad, shape[0], shape[1])

    imgRec[:, :, 0] = R
    imgRec[:, :, 1] = G
    imgRec[:, :, 2] = B

    #print(imgRec)

    return imgRec, Y

#-------------------------------------------------------------------------------------------
def main():
    fName = "./imagens/airport.bmp"
    img = plt.imread(fName)
    quality = 75
    interpolation_method = cv2.INTER_LINEAR   # cv2.INTER_NEAREST ** cv2.INTER_CUBIC ** cv2.INTER_LANCZOS4

    shape = img.shape

    showImg(img, "Imagem Original")

    print(type(img))

    Y_dpcm, Cb_dpcm, Cr_dpcm, Yo = encoder(img, shape, quality, interpolation_method)

    imgRec, Yr = decoder(Y_dpcm, Cb_dpcm, Cr_dpcm, shape, quality, interpolation_method)
    showImg(imgRec, "Imagem Reconstruida")
    print("==================================================================================")
    print("Imagem Reconstruida")
    showSubMatriz(imgRec, 8, 8, 8)

    # EXERCÍCIO 10 -------------------------------------------------------------------------------------------
    diff_Y(Yo, Yr, img, imgRec, quality)


if __name__ == "__main__":
    main()
