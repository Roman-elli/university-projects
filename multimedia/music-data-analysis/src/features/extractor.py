import librosa #https://librosa.org/    # sudo apt-get install -y ffmpeg (open mp3 files)
import config as cfg
import numpy as np
import scipy.stats as stats

def features(soundFolder, testMusics):
    feature_list = np.zeros((cfg.song_list_size, 190))
    centroid_librosa = []
    for  i in range(cfg.song_list_size):
        y, fs = librosa.load(soundFolder +'/'+testMusics[i], cfg.sr, cfg.mono)
        fmax = fs/2
            
        mfcc = librosa.feature.mfcc(y=y, n_mfcc=13)
        feature_list[i, 0:91] = statistics(mfcc)
        sc = librosa.feature.spectral_centroid(y = y)
        feature_list[i, 91:98] = statistics(sc)
        
        centroid_librosa.append(sc[0][2:])
        
        sb = librosa.feature.spectral_bandwidth(y=y)
        feature_list[i, 98:105] = statistics(sb)
        
        sco = librosa.feature.spectral_contrast(y=y)
        feature_list[i, 105:154] = statistics(sco)
        sf = librosa.feature.spectral_flatness(y=y)
        feature_list[i, 154:161] = statistics(sf)
        sro = librosa.feature.spectral_rolloff(y=y)
        feature_list[i, 161:168] = statistics(sro)
        
        fo = librosa.yin(y=y, fmin = 20, fmax = fmax)
        fo[fo == fmax] = 0
        feature_list[i, 168:175] = statistics(np.array((fo, )))
        rms = librosa.feature.rms(y=y)
        feature_list[i, 175:182] = statistics(rms)
        zcr = librosa.feature.zero_crossing_rate(y=y)
        feature_list[i, 182:189] = statistics(zcr)
        
        feature_list[i, 189] = librosa.feature.tempo(y=y)
        
    return feature_list, centroid_librosa
 
def statistics(features):
    size_feature = features.shape[0]
    statistic_list = np.zeros((size_feature, 7))
    for i in range (size_feature):
        feature = features[i]
        if len(features[i]) == 0:
            continue
        statistics_values = [
            np.mean(feature),
            np.std(feature),
            stats.skew(feature),
            stats.kurtosis(feature),
            np.median(feature),
            np.max(feature),
            np.min(feature)
        ]
        statistic_list[i] = statistics_values
    return_statistics = np.array(statistic_list).flatten()
    return return_statistics
