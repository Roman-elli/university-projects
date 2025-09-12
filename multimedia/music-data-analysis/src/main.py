import librosa #https://librosa.org/    # sudo apt-get install -y ffmpeg (open mp3 files)
import librosa.display
import librosa.beat
import sounddevice as sd
import warnings
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
import math
import config as cfg


def features(soundFolder, testMusics):
    feature_list = np.zeros((cfg.song_list_size, 190))
    centroid_librosa = []
    for  i in range(cfg.song_list_size):
        y, fs = librosa.load(soundFolder+'/'+testMusics[i], cfg.sr, cfg.mono)
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
        
    np.savetxt("spectral_metrics.csv", compare, '%.6f', ',')

def euclidian_distance(object1, object2):
    return_result = np.sum(math.pow((object1 - object2), 2))
    return math.sqrt(return_result)

def manhattan_distance(object1, object2):
    return_result = np.sum(abs(object1 - object2))
    return return_result

def cosine_distance(object1, object2):
    cosine_top = np.sum(object1 * object2)
    cosine_bottom_left = np.sum(math.pow(object1, 2))
    cosine_bottom_right = np.sum(math.pow(object2, 2))
    return (1 - cosine_top/(math.sqrt(cosine_bottom_left)*math.sqrt(cosine_bottom_right)))

def get_distances():
    query_results = np.genfromtxt("./validação de resultados_TP2/notNormFM_Q.csv", delimiter=',')
    all_results = np.genfromtxt("./validação de resultados_TP2/FM_All.csv", delimiter=',')
    normalized_query_results = np.zeros_like(query_results)
    distances = np.zeros((900, 3))
    for i in range(len(normalized_query_results)):
        if (all_results[0,i] != all_results[1,i]):
            normalized_query_results[i] = (query_results[i] - all_results[0,i]) / (all_results[1,i] - all_results[0,i])

    for i in range(len(all_results[2:902, :])):
        distances[i,0] = euclidian_distance(normalized_query_results, all_results[i+2,:])
        distances[i,1] = manhattan_distance(normalized_query_results, all_results[i+2,:])
        distances[i,2] = cosine_distance(normalized_query_results, all_results[i+2,:])
    np.savetxt("de_r.csv", distances[:,0], '%.6f', ',')
    np.savetxt("dm_r.csv", distances[:,1], '%.6f', ',')
    np.savetxt("dc_r.csv", distances[:,2], '%.6f', ',')
    return

def ranking_similarity():
    dist_euclidiana = np.loadtxt("de_r.csv", delimiter=",")
    dist_manhattan = np.loadtxt("dm_r.csv", delimiter=",")
    dist_coseno = np.loadtxt("dc_r.csv", delimiter=",")
    
    soundFolder = "./Music"
    testMusics = np.array(os.listdir(soundFolder))
    
    top10_euclidiana = np.argsort(dist_euclidiana)[:10]
    top10_manhattan = np.argsort(dist_manhattan)[:10]
    top10_coseno = np.argsort(dist_coseno)[:10]
    
    euclidean_files = testMusics[top10_euclidiana]
    euclidean_dists = dist_euclidiana[top10_euclidiana]
    
    manhattan_files = testMusics[top10_manhattan]
    manhattan_dists = dist_manhattan[top10_manhattan]
    
    cosine_files = testMusics[top10_coseno]
    cosine_dists = dist_coseno[top10_coseno]
    
    with open("rankings.txt", "w") as f:
        f.write("Ranking: Euclidean-------------\n")
        np.savetxt(f, [euclidean_files], fmt='%s')
        np.savetxt(f, [euclidean_dists], fmt='%.6f')
        
        f.write("\nRanking: Manhattan-------------\n")
        np.savetxt(f, [manhattan_files], fmt='%s')
        np.savetxt(f, [manhattan_dists], fmt='%.6f')
        
        f.write("\nRanking: Cosine-------------\n")
        np.savetxt(f, [cosine_files], fmt='%s')
        np.savetxt(f, [cosine_dists], fmt='%.6f')
        
    return euclidean_files, manhattan_files, cosine_files

def metadata_query():
    query_metadata = np.genfromtxt("./query_metadata.csv", delimiter = ',', dtype = str)
    all_metadata = np.genfromtxt("./panda_dataset_taffc_metadata.csv", delimiter = ',', dtype = str)
    equals = np.zeros(900)
    important_qm_artist = query_metadata[1, 1]
    important_qm_moods = np.array(query_metadata[1, 9][1:-1].split("; "))
    important_qm_genre = np.array(query_metadata[1, 11][1:-1].split("; "))
    important_am = np.array([all_metadata[1:, 1], all_metadata[1:, 9], all_metadata[1:, 11]])

    for specific_data in range(important_am.shape[1]):
        if (important_am[0, specific_data] == important_qm_artist):
            equals[specific_data] = 1

        for mood in important_qm_moods:
            equals[specific_data] += important_am[1, specific_data].count(mood)
        
        for genre in important_qm_genre:
            equals[specific_data] += important_am[2, specific_data].count(genre)
            
    top10 = np.flip(np.array(equals.argsort()[-11:-1]))
    top_files = all_metadata[top10+1, 0]
    top_scores = equals[top10]
    
    top_files_clean = [str(file).strip().strip('"') + '.mp3' for file in top_files]  

    with open("rankings.txt", "a") as f:
        f.write("\nRanking: Metadata-------------\n")
        np.savetxt(f, [top_files_clean], fmt='%s')
        np.savetxt(f, [top_scores], fmt='%.0f')
    
    return top_files_clean

def precision(metadata, euclidean, manhattan, cosine):
    count_euclidean = 0
    count_manhattan = 0
    count_cosine = 0

    for i in range(10):
        if euclidean[i] in metadata:
            count_euclidean += 1
        if manhattan[i] in metadata:
            count_manhattan += 1
        if cosine[i] in metadata:
            count_cosine += 1

    prec_euclidean = count_euclidean / 10 * 100
    prec_manhattan = count_manhattan / 10 * 100
    prec_cosine = count_cosine / 10 * 100
    
    with open("rankings.txt", "a") as f:
        f.write(f"\nPrecision de: {prec_euclidean:.1f}\n")
        f.write(f"Precision dm: {prec_manhattan:.1f}\n")
        f.write(f"Precision dc: {prec_cosine:.1f}\n")
    return 

def main():
    plt.close('all')
    
    fName = "./Queries/MT0000414517.mp3"
    soundFolder = "./Music"    
    warnings.filterwarnings("ignore")
    testMusics = os.listdir(soundFolder)
    
    feature_list, centroid_librosa = features(soundFolder, testMusics)

    normalized_features = normalize_features(feature_list)

    np.savetxt("features_info.csv", normalized_features, '%.6f', ',')
    
    spectral_centroid(soundFolder, testMusics, centroid_librosa)
    
    get_distances()

    euclidean, manhattan, cosine = ranking_similarity()
    
    metadata = metadata_query()

    precision(metadata, euclidean, manhattan, cosine)
    
if __name__ == "__main__":
   main()