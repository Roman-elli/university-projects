import numpy as np
import config as cfg

def normalize_features(feature_list):
    normalized_features = np.zeros((cfg.song_list_size + 2, 190))
    for i in range (feature_list.shape[1]):
        normalized_features[0][i] = np.min(feature_list[:,i])
        normalized_features[1][i] = np.max(feature_list[:,i])

        if normalized_features[0][i] == normalized_features[1][i]:
            normalized = np.zeros_like(feature_list.shape[1])
        else:
            normalized = (feature_list[:,i] - normalized_features[0][i]) / (normalized_features[1][i] - normalized_features[0][i])
        
        normalized_features[2:902, i] = normalized
    return normalized_features
