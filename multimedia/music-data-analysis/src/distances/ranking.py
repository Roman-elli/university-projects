import os
import numpy as np
from metrics import *
from utils.io import load_csv, save_csv, write_ranking

def get_distances():
    query_results = load_csv("data/validação de resultados_TP2/notNormFM_Q.csv", delimiter=',')
    all_results = load_csv("data/validação de resultados_TP2/FM_All.csv", delimiter=',')
    
    normalized_query_results = np.zeros_like(query_results)
    distances = np.zeros((900, 3))
    
    for i in range(len(normalized_query_results)):
        if (all_results[0,i] != all_results[1,i]):
            normalized_query_results[i] = (query_results[i] - all_results[0,i]) / (all_results[1,i] - all_results[0,i])

    for i in range(len(all_results[2:902, :])):
        distances[i,0] = euclidian_distance(normalized_query_results, all_results[i+2,:])
        distances[i,1] = manhattan_distance(normalized_query_results, all_results[i+2,:])
        distances[i,2] = cosine_distance(normalized_query_results, all_results[i+2,:])
    
    save_csv("de_r.csv", distances[:,0], '%.6f', ',')
    save_csv("dm_r.csv", distances[:,1], '%.6f', ',')
    save_csv("dc_r.csv", distances[:,2], '%.6f', ',')

    return

def ranking_similarity():
    dist_euclidiana = load_csv("de_r.csv")
    dist_manhattan = load_csv("dm_r.csv")
    dist_coseno = load_csv("dc_r.csv")
    
    soundFolder = "data/samples"
    testMusics = np.array(os.listdir(soundFolder))
    
    top10_euclidiana = np.argsort(dist_euclidiana)[:10]
    top10_manhattan = np.argsort(dist_manhattan)[:10]
    top10_coseno = np.argsort(dist_coseno)[:10]
    
    euclidean_files, euclidean_dists = testMusics[top10_euclidiana], dist_euclidiana[top10_euclidiana]
    manhattan_files, manhattan_dists = testMusics[top10_manhattan], dist_manhattan[top10_manhattan]
    cosine_files, cosine_dists = testMusics[top10_coseno], dist_coseno[top10_coseno]
    
    write_ranking("data/rankings.txt", "Ranking: Euclidean-------------", euclidean_files, euclidean_dists)
    write_ranking("data/rankings.txt", "Ranking: Manhattan-------------", manhattan_files, manhattan_dists)
    write_ranking("data/rankings.txt", "Ranking: Cosine-------------", cosine_files, cosine_dists)
    
    return euclidean_files, manhattan_files, cosine_files