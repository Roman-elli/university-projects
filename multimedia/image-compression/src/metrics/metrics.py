import numpy as np
import config as cfg

from utils.io import saveImg

def diff_Y(Yo, Yr, img, imgRec, quality, output_folder):
    diff = np.abs(Yo - Yr)

    diff = (diff / np.max(diff)) * 255 if np.max(diff) > 0 else diff
    diff = diff.astype(np.uint8)

    saveImg(diff, output_folder, "image_diferences", cfg.cm_gray)

    img = img.astype(np.uint16)

    mse = np.sum((img - imgRec) ** 2) / (img.shape[0] * img.shape[1])

    rmse = np.sqrt(mse)

    P = np.sum(img**2) / (img.shape[0] * img.shape[1])

    snr = 10*np.log10(P/mse)

    psnr = 10*np.log10((np.max(img)) **2/mse)

    print(f"=======================================")
    print("Compression Quality", quality)
    print("Max Diff: ", np.max(diff))
    print("Avg Diff: ", np.mean(diff))
    print("MSE: ", mse)
    print("RMSE: ", rmse)
    print("SNR: ", snr)
    print("PSNR: ", psnr)
    print(f"=======================================")
