import numpy

from lib.classes import SVDResult


def numpy_SVD(matrix: numpy.ndarray, r: int) -> SVDResult:
    U, S, Vh = numpy.linalg.svd(matrix, full_matrices=False)
    return SVDResult(U[:, 0:r], S[0:r], Vh[0:r, :])
