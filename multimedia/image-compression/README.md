# 🖼️ Image Compression – JPEG-like Encoder & Decoder

This project was developed during my **Multimedia Systems** university course.  
It implements a simplified **JPEG-like image compression algorithm**, including color space conversion, subsampling, DCT, quantization, and DPCM coding.

---

## 🚀 Features

🔹 **Color Space Conversion**  
  RGB → YCbCr and back.

🔹 **Subsampling**  
  Supports chroma subsampling (4:2:0 style).

🔹 **DCT Transform**  
  Applies 2D Discrete Cosine Transform both globally and block-based.

🔹 **Quantization / Dequantization**  
  Adjustable compression quality factor.

🔹 **DPCM Encoding / Decoding**  
  Predictive coding applied to DC coefficients.

🔹 **Reconstruction & Metrics**  
  Rebuilds the image and computes **MSE, RMSE, SNR, and PSNR**.

🔹 **Difference Visualization**  
  Saves a **difference image (Yo − Yr)**, showing pixel-level distortion after compression.

🔹 **File Support**  
  Works with `.bmp`, `.png`, `.jpg`, `.jpeg`.

---

## 🕹️ How to Run

1. Place input images inside: assets/images/

2. Run the program:
    ```bash
    python src/main.py
    ```

3. Select an image from the menu to compress & decompress. 
    - Results are saved inside: data/images/<image_name>/
