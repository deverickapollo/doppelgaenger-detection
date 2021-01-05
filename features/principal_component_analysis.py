import numpy as np


# transform a dictionary to a numpy array
def get_numpy_array(dict):
    matrix = list(dict.values())
    numpy_matrix = np.array([list for list in matrix])
    return numpy_matrix


# tranpose a numpy array
def transpose_matrix(matrix):
    return matrix.T


# normalize a matrixs columns to values between 0 and 1
def normalize_matrix(matrix):
    x_normed = matrix / matrix.max(axis=0)
    return x_normed


# calculate the covariance matrix for a matrix where each column represents a variable
def get_covariance_matrix(matrix):
    cov_matrix = np.cov(matrix, rowvar=False)
    return cov_matrix


# calculate the eigenvectors and eigenvalues for a matrix
def get_eigen(matrix):
    return np.linalg.eig(matrix)


# return the eigenvectors for the most principal components (minimal error between the original
# dataset and the PCA > 0.999)
def get_most_principal_components(matrix_eig):
    t = len(matrix_eig[0])+1
    for i in reversed(range(len(matrix_eig[0])+1)):
        if sum(matrix_eig[0][:i]) / sum(matrix_eig[0]) > 0.999:
            t = i
    return matrix_eig[1][:t]


# execute principal component analysis
# input: feature matrix as a dict where each key represents a variable
# output: reduced feature matrix where each column represents a principal component
def execute_pca(dict):
    matrix = get_numpy_array(dict)
    user_ids = matrix[-1][:,None]
    matrix = transpose_matrix(matrix[:-1])
    matrix_norm = normalize_matrix(matrix)
    matrix_norm_cov = get_covariance_matrix(matrix_norm)
    matrix_norm_cov_eigen = get_eigen(matrix_norm_cov)
    matrix_reduced = matrix.dot(transpose_matrix(get_most_principal_components(matrix_norm_cov_eigen)))
    return np.append(matrix_reduced, user_ids, axis=1)
