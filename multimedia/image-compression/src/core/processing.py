from utils.io import saveImg
from core.codec import encoder, decoder
from metrics.metrics import diff_Y

def process_image(img, shape, quality, interpolation_method, output_folder):
    saveImg(img, output_folder, "original_image")
    
    Y_dpcm, Cb_dpcm, Cr_dpcm, Yo = encoder(img, shape, quality, interpolation_method, output_folder)
    imgRec, Yr = decoder(Y_dpcm, Cb_dpcm, Cr_dpcm, shape, quality, interpolation_method, output_folder)
    
    saveImg(imgRec, output_folder,"reconstructed_image")
    diff_Y(Yo, Yr, img, imgRec, quality, output_folder)
    
    return imgRec