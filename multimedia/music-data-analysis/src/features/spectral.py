import librosa #https://librosa.org/    # sudo apt-get install -y ffmpeg (open mp3 files)
import numpy as np
import config as cfg
from utils.io import save_csv


def spectral_centroid(soundFolder, testMusics, centroid_librosa):
    feature_centroid = []
    compare = np.zeros((cfg.song_list_size, 2))

    for i in range(cfg.song_list_size):
        y, fs = librosa.load(f"{soundFolder}/{testMusics[i]}", cfg.sr, cfg.mono)
        sample = np.array(y)
        points = len(sample) % cfg.jump_counter
        if points == 0: n = 0 
        else: n = cfg.jump_counter - points
        n_padding = len(sample) + n 
        sample = np.append(sample, np.zeros(n))

        n_windows = n_padding // cfg.jump_counter - 3
        centroid = np.zeros(n_windows)

        for j in range(n_windows):
            start = j * cfg.jump_counter
            end = start + 2048
            window = sample[start:end]

            window_hann = window * np.hanning(len(window))

            magnitude = np.abs(np.fft.rfft(window_hann))
            freqs = np.fft.rfftfreq(len(window_hann), 1 / fs)

            denominator = np.sum(magnitude)
            if denominator == 0:
                centroid_sample = 0
            else:
                centroid_sample = np.sum(freqs * magnitude) / denominator

            centroid[j] = centroid_sample

        feature_centroid.append(centroid)
        
        sc_librosa = centroid_librosa[i]
        fc = feature_centroid[i]

        min_len = min(len(sc_librosa), len(fc))
        sc_librosa = sc_librosa[:min_len]
        fc = fc[:min_len]
        print("fc:", len(fc))
        print("sc_librosa:", len(sc_librosa))

        pearson = np.corrcoef(sc_librosa, fc)[0,1] 
        compare[i, 0] = pearson

        rmse = np.sqrt(np.mean((sc_librosa - fc) ** 2))
        compare[i, 1] = rmse
        
    save_csv("data/spectral_metrics.csv", compare, '%.6f', ',')
