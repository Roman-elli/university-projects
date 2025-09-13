import warnings
import matplotlib.pyplot as plt
import os

from features.extractor import features
from features.normalization import normalize_features
from features.spectral import spectral_centroid
from distances.ranking import ranking_similarity, get_distances
from evaluation.metadata import metadata_query, precision
from utils.io import save_csv

def main():
    plt.close('all')
    
    fName = "assets/sounds/MT0000414517.mp3"
    soundFolder = "data/samples"    
    warnings.filterwarnings("ignore")
    testMusics = os.listdir(soundFolder)
    
    feature_list, centroid_librosa = features(soundFolder, testMusics)

    normalized_features = normalize_features(feature_list)

    save_csv("data/features_info.csv", normalized_features, '%.6f', ',')
    
    spectral_centroid(soundFolder, testMusics, centroid_librosa)
    
    get_distances()

    euclidean, manhattan, cosine = ranking_similarity()
    
    metadata = metadata_query()

    precision(metadata, euclidean, manhattan, cosine)
    
if __name__ == "__main__":
   main()