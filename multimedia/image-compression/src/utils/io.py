import os
import matplotlib.pyplot as plt
import numpy as np

def saveImg(img, folder, title, cmap=None):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{title}.png")
    
    if img.ndim == 2:
        plt.imsave(path, img, cmap=cmap)
    else:
        plt.imsave(path, img.astype(np.uint8))
    
    print(f"💾 Saved: {path}")
