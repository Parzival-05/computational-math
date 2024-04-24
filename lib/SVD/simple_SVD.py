import numpy as np
from numpy.linalg import norm

from random import normalvariate
from math import sqrt
from lib.classes import SVDResult


def randomUnitVector(n):
    unnormalized = [normalvariate(0, 1) for _ in range(n)]
    theNorm = sqrt(sum(x * x for x in unnormalized))
    return [x / theNorm for x in unnormalized]


def svd_1d(A, epsilon=1e-10):
    m, n = A.shape
    x = randomUnitVector(min(m, n))
    lastV = None
    currentV = x

    if m > n:
        B = np.dot(A.T, A)
    else:
        B = np.dot(A, A.T)

    iterations = 0
    while True:
        iterations += 1
        lastV = currentV
        currentV = np.dot(B, lastV)
        currentV_norm = norm(currentV)
        if currentV_norm > 0:
            currentV = currentV / currentV_norm  # делим только если норма больше 0
        else:
            return currentV

        if abs(np.dot(currentV, lastV)) > 1 - epsilon:
            return currentV


def simple_SVD(A, k, epsilon=1e-10):
    A = np.array(A, dtype=float)
    n, m = A.shape
    svdSoFar = []

    for i in range(k):
        matrixFor1D = A.copy()

        for singularValue, u, v in svdSoFar[:i]:
            matrixFor1D -= singularValue * np.outer(u, v)

        if n > m:
            v = svd_1d(matrixFor1D, epsilon=epsilon)  # next singular vector
            u_unnormalized = np.dot(A, v)
            sigma = norm(u_unnormalized)  # next singular value
            u = u_unnormalized / sigma
        else:
            u = svd_1d(matrixFor1D, epsilon=epsilon)  # next singular vector
            v_unnormalized = np.dot(A.T, u)
            sigma = norm(v_unnormalized)  # next singular value
            v = v_unnormalized / sigma

        svdSoFar.append((sigma, u, v))

    singularValues, us, vs = [np.array(x) for x in zip(*svdSoFar)]
    return SVDResult(us.T, singularValues, vs)
