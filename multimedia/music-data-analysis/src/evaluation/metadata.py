import numpy as np
import config as cfg
from utils.io import append_precision, load_csv


def metadata_query():
    query_metadata = load_csv("./query_metadata.csv", delimiter = ',', dtype = str)
    all_metadata = load_csv("./panda_dataset_taffc_metadata.csv", delimiter = ',', dtype = str)
    
    equals = np.zeros(cfg.song_list_size)
    
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
    
    append_precision("data/rankings.txt", prec_euclidean, prec_manhattan, prec_cosine)

    return 
