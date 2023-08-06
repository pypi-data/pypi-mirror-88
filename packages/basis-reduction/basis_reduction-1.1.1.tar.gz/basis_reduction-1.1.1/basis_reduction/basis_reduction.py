from math import sqrt
from math import floor
from math import fabs
from math import ceil
import numpy as np

def norm(vector):
    vector = np.array(vector)
    return np.linalg.norm(vector)

def dot(vector1, vector2):
    vector1 = np.array(vector1, float)
    vector2 = np.array(vector2, float)
    return np.dot(vector1, vector2)

def shortest_vector(vectors):
    assert len(vectors) != 0
    vectors = np.array(vectors)
    min_norm = None
    index_shortest = None
    vector_norm = None
    for i in range(len(vectors)):
        vector_norm = norm(vectors[i])
        if min_norm == None or vector_norm < min_norm:
            min_norm = vector_norm
            vector_norm = None
            index_shortest = i
    return vectors[index_shortest]

def mu(vector1, vector2):      
    vector1 = np.array(vector1, float)
    vector2 = np.array(vector2, float)
    
    dot_vector1_vector2 = dot(vector1, vector2)
    dot_self_vector2 = dot(vector2, vector2)
    
    assert dot_self_vector2 != 0
    
    return (dot_vector1_vector2/dot_self_vector2)

def mu_indices(mu_coeffs, k, j):
    return mu_coeffs[k + j -1]

def gaussian_reduction(vector1, vector2):

    vectorCont = []
    q = 0
    
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    
    while True:
        
        if norm(vector1) > norm(vector2):
            vectorCont = vector1
            vector1 = vector2
            vector2 = vectorCont
            
        q = floor(dot(vector2, vector1/dot(vector1, vector1)))
            
        if q == 0:
            break
            
        vector2 = vector2 - vector1*q
        
    return [vector1, vector2]

def gramshmidt(vectors, orthonormalization = False):
    vectors = np.array(vectors)        
    orth_vectors = []
    vector = np.array([])
    mu_coeff = 0.0
    mu_coeffs = []
    result = {}
    
    if len(vectors) == 0:
        return orth_vectors
    
    for i in range(len(vectors)):
        
        if i == 0:
            vector = vectors[i]
        else:
            vector = vectors[i]
            for j in range(len(orth_vectors)):
                mu_coeff = mu(vectors[i], orth_vectors[j])
                vector = vector - mu_coeff*orth_vectors[j]
                mu_coeffs.append(mu_coeff)

            mu_coeff = 0.0
           
        if orthonormalization:
            vector = vector/norm(vector)
            
        orth_vectors.append(vector)
        vector = np.array([])
    
    mu_coeffs = np.array(mu_coeffs)
    orth_vectors = np.array(orth_vectors)
    
    result['basis'] = orth_vectors
    result['mu_coeffs'] = mu_coeffs
    result['orthonormalization'] = orthonormalization
            
    return result

def lll_reduction(vectors, y):
    
    vectors = np.array(vectors)
    vectors_orth = gramshmidt(vectors)['basis']
    d = len(vectors)
    k = 1
    
    while k < d:
        
        for j in range(k - 1, -1, -1):
            mu_kj = mu(vectors[k], vectors_orth[j])

            if fabs(mu_kj) > 0.5:
                vectors[k] = vectors[k] - vectors[j] * round(mu_kj)
                vectors_orth = gramshmidt(vectors)['basis']
                    
        if (y - mu(vectors[k], vectors[k-1])**2) * dot(vectors_orth[k-1], vectors_orth[k-1]) <= dot(vectors_orth[k], vectors_orth[k]):
            k += 1
        else:
            vectors[[k, k-1]] = vectors[[k-1, k]]                
            vectors_orth = gramshmidt(vectors)['basis']
            k = max(k - 1, 1)
    
    return vectors


def check_lll_reduction(vectors, y):
    
    vectors = np.array(vectors, float)
    gramshmidt_result = gramshmidt(vectors)
    vectors_orth = gramshmidt_result['basis']
    mu_coeffs = gramshmidt_result['mu_coeffs']
    
    # первое условие
    for mu in mu_coeffs:
        if mu > 0.5:
            return False
        
    # второе условие
    for i in range(len(vectors)):
        if i > 0:
            
            left_part = norm(vectors[i] + mu_indices(mu_coeffs, k, (k-1))*vectors[i-1])**2
            rigth_part = y*(norm(vectors[i-1])**2)
            
            if left_part < rigth_part:
                return False
        
    return True
