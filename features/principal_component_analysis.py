import scipy.linalg as la
import numpy as np

# calculate the covariance matrix for a matrix
def get_covariance_matrix(matrix):
    m = list(matrix.values())
    cov_matrix = np.cov(m)
    return cov_matrix

# calculate the eigenvectors and eigenvalues for a matrix
# returns a tuple (eigenvalues, eigenvectors)
def get_eigenvectors_eigenvalues(matrix):
    eig = la.eig(matrix)
    return eig


