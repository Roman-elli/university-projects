import os
import config as cfg

from utils.utils import prepare_image
from core.processing import process_image
from ui.menu import menu

def main():
    folder = cfg.IMAGE_PATH
    files = [f for f in os.listdir(folder) if f.lower().endswith((".bmp", ".png", ".jpg", ".jpeg"))]

    if not files:
        print("⚠️ No image files found in assets/images/")
        print(f"=======================================")
        return

    while True:
        choice = menu(files)

        if choice == 0:
            break

        img, output_folder, filename_no_ext = prepare_image(folder, files[choice-1])
        shape = img.shape
        quality = cfg.quality
        interpolation_method = cfg.linear_interpolation_method

        process_image(img, shape, quality, interpolation_method, output_folder)

        print(f"✅ Compression of '{filename_no_ext}' completed successfully!")
        print(f"=======================================")

if __name__ == "__main__":
    main()
