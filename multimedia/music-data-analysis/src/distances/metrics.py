import math
import numpy as np

def euclidian_distance(object1, object2):
    return_result = np.sum(np.power((object1 - object2), 2))
    return np.sqrt(return_result)

def manhattan_distance(object1, object2):
    return_result = np.sum(abs(object1 - object2))
    return return_result

def cosine_distance(object1, object2):
    cosine_top = np.sum(object1 * object2)
    cosine_bottom_left = np.sum(np.power(object1, 2))
    cosine_bottom_right = np.sum(np.power(object2, 2))
    return (1 - cosine_top/(math.sqrt(cosine_bottom_left)*math.sqrt(cosine_bottom_right)))
