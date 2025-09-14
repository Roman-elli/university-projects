# 🎵 Music Retrieval – Distance-Based Similarity Search

This project was developed during my **Multimedia Systems** university class.  
It implements a **music similarity retrieval system** based on feature normalization and distance metrics.

---

## 🚀 Features

🔹 **Feature Normalization**  
  Normalizes query features against global dataset statistics.  

🔹 **Distance Metrics**  
  Computes **Euclidean, Manhattan, and Cosine** distances.  

🔹 **Ranking System**  
  Generates top-10 rankings for each distance metric.  

🔹 **Precision Evaluation**  
  Calculates retrieval precision at top-10 for all metrics.  

🔹 **CSV & TXT Support**  
  Loads feature matrices from `.csv` files and writes results/rankings to `.txt` reports.  

🔹 **Audio Dataset Integration**  
  Works with pre-extracted feature vectors from music samples.  

---

## 📂 Project Structure

- **`assets/samples/`** 🎶  
  Contains **200 example audio files** used as the dataset for feature extraction and similarity search.  

- **`assets/validation/`** 📑  
  Holds **validation CSV files** documenting feature matrices and ground-truth data for evaluation.  

- **`data/`** 💾  
  Stores all **generated outputs** during execution (feature info, spectral metrics, distance results, rankings, and precision reports).  

---

## 🕹️ How to Run

1. Place input files inside:  
   - Features: `assets/validation/`  
   - Audio samples: `assets/samples/`

2. Install dependencies 
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. Run the program:
    ```bash
    python src\main.py
    ```

4. Rankings and evaluation results will be saved in:
    ```bash
    data/rankings.txt
    ```