import numpy as np
from numpy.linalg import norm

from lib.SVD.simple_SVD import simple_SVD
from lib.classes import SVDResult


def advanced_SVD(A, rank):
    n_samples = 2 * rank

    _, n = A.shape
    O = np.random.randn(n, n_samples)
    Y = A @ O
    Q, _ = np.linalg.qr(Y)

    B = Q.T @ A
    svd = simple_SVD(B, rank)
    U = Q @ svd.U
    return SVDResult(U, svd.S, svd.Vh)
