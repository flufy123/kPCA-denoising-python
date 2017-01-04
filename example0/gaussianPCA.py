from scipy.spatial.distance import pdist, squareform
from scipy import exp
from scipy.linalg import eigh
import numpy as np

def stepwise_kpca(X, gamma, n_components):
    """
    Implementation of a RBF kernel PCA.

    Arguments:
        X: A lxN dataset as NumPy array where the samples are stored as rows (l),
           and the attributes defined as columns (N).
        gamma: A free parameter (coefficient) for the gaussian kernel.
        n_components: The number of components to be returned.
    """
    # Calculating the squared Euclidean distances for every pair of points
    # in the MxN dimensional dataset.
    sq_dists = pdist(X, 'sqeuclidean')

    # Converting the pairwise distances into a symmetric MxM matrix.
    mat_sq_dists = squareform(sq_dists)

    # Computing the lxl kernel matrix.
    K = exp(-gamma * mat_sq_dists)

    # Centering the symmetric lxl kernel matrix.
    l = K.shape[0]
    one_n = np.ones((l, l)) / l
    K = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)

    # Obtaining eigenvalues in descending order with corresponding
    # eigenvectors from the symmetric matrix.
    # corresponds to lambda and alpha from the eq. (3) in the paper.
    eigvals, eigvecs = eigh(K)

    # Obtaining the i eigenvectors that corresponds to the i highest eigenvalues.
    X_pc = np.column_stack((eigvecs[:, -i] for i in range(1, n_components + 1)))

    return X_pc