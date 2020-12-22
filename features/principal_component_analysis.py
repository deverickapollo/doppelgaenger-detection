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
def eigen(matrix):
    return np.linalg.eig(matrix)


# return the the value K (new dimension) for the best low-dimensional feature space (minimal error between the original
# dataset and the PCA > 0.999)
def feature_reduction(matrix_eigenvalues):
    t = len(matrix_eigenvalues)+1
    for i in reversed(range(len(matrix_eigenvalues)+1)):
        if sum(matrix_eigenvalues[:i]) / sum(matrix_eigenvalues) > 0.999:
            t = i
    return t