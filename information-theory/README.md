# 📂 GZIP Decompressor  

I developed this project during my university studies. It was implemented in **Python** and reproduces the logic of a **GZIP decompressor**, decoding data compressed with the **Deflate algorithm (Huffman + LZ77)**.  

It allows you to **select a category (image, sound, or text)**, choose a file, and decompress it to recover the original data.  

---

## 🚀 Features
- 📑 **Reads and validates GZIP headers** (ID1, ID2, compression method, flags, extra fields, etc.).  
- 🧩 **Implements Huffman coding and decoding** with dynamic trees.  
- 🔄 **Supports block-by-block decompression** of Deflate streams.   
- 📜 Menu-driven interface:
  - Choose file type  
  - List available files  
  - Decompress selected file  
- 💾 Saves decompressed output automatically in the `data/` folder.  

---

## 🕹️ Main Menu
- When running the program, you will see:  
1. Image
2. Sound
3. Text
4. Exit

- After choosing a category, you will get a **list of files available in that folder**. Then, select one to decompress.

---

## ▶️ How to Run
1. Clone or download the project.  

2. Install requirements (only **NumPy** is needed):
   ```bash
   pip install numpy
   ```

3. Run the program:
    ```bash
    python gzip_compressor.py
    ```

4. The decompressed file will be stored automatically in the data/ folder, keeping the original filename.

---

## 📌 Notes

- Only files compressed with Deflate (Huffman dynamic coding) are supported.
- The project is for academic/learning purposes, showcasing how GZIP works internally.
- In this repository already have some examples to test in the `assets/` folder.