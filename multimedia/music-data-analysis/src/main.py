import warnings
import matplotlib.pyplot as plt
import os
import config as cfg

from features.extractor import features
from features.normalization import normalize_features
from features.spectral import spectral_centroid
from distances.ranking import ranking_similarity, get_distances
from evaluation.metadata import metadata_query, precision
from utils.io import save_csv

def main():
    plt.close('all')
    
    warnings.filterwarnings("ignore")
    testMusics = os.listdir(cfg.SAMPLES_PATH)
    
    print("🚀 Starting Music Retrieval Pipeline...")

    feature_list, centroid_librosa = features(cfg.SAMPLES_PATH, testMusics)
    print("🎵 Features extracted & statistics computed")

    normalized_features = normalize_features(feature_list)
    print("📊 Features normalized successfully")

    save_csv("features_info.csv", normalized_features, '%.6f', ',')
    print("💾 Normalized features saved to CSV")

    spectral_centroid(cfg.SAMPLES_PATH, testMusics, centroid_librosa)
    print("🎼 Spectral centroid processed successfully")

    get_distances()
    print("📏 Distance metrics (Euclidean, Manhattan, Cosine) calculated")

    euclidean, manhattan, cosine = ranking_similarity()
    print("🏆 Similarity rankings (Top-10) generated")

    metadata = metadata_query()
    print("📝 Metadata-based recommendations retrieved")

    precision(metadata, euclidean, manhattan, cosine)
    print("✅ Precision metrics evaluated and saved")

    print("🎯 Music Retrieval Pipeline completed successfully!")

    
if __name__ == "__main__":
   main()