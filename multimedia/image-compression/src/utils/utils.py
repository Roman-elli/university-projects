import os
import numpy as np
import matplotlib.pyplot as plt

from utils.io import saveImg
from metrics.metrics import diff_Y

def padding(matriz, nl, nc, dim):
    addLine = dim - (nl % dim)
    addColumn = dim - (nc % dim)

    ultima_linha = matriz[-1, :]
    matrizLine = np.tile(ultima_linha, (addLine, 1))
    matriz = np.vstack((matriz, matrizLine))

    ultima_coluna = matriz[:, -1]
    matrizColumn = np.tile(ultima_coluna[:, None], (1, addColumn))
    matriz = np.hstack((matriz, matrizColumn))
    return matriz

def despadding(matriz, nl, nc):
    return matriz[:nl, :nc]

def prepare_image(folder, filename):
    fName = os.path.join(folder, filename)

    print(f"\n👉 Selected image: {fName}")
    print(f"=======================================")

    filename_no_ext = os.path.splitext(filename)[0]
    output_folder = os.path.join("data/images", filename_no_ext)
    os.makedirs(output_folder, exist_ok=True)

    img = plt.imread(fName)

    return img, output_folder, filename_no_ext

