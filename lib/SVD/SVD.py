import numpy

from lib.SVD.numpy_SVD import numpy_SVD
from lib.SVD.simple_SVD import simple_SVD
from lib.SVD.advanced_SVD import advanced_SVD
from lib.classes import ArgError, SVDResult
from lib.consts import Method


def SVD(matrix: numpy.ndarray, r: int, method: str) -> SVDResult:
    dim = numpy.ndim(matrix)
    match method:
        case Method.NUMPY:
            svd = numpy_SVD
        case Method.SIMPLE:
            svd = simple_SVD
        case Method.ADVANCED:
            svd = advanced_SVD
        case _:
            raise ArgError("method")
    if dim == 2:
        return svd(matrix, r)
    elif dim >= 3:
        unpack = lambda svd: (svd.U, svd.S, svd.Vh)
        SVDs = map(lambda x: unpack(SVD(x, r, method)), matrix)
        U, S, Vh = list(map(numpy.array, list(zip(*SVDs))))
        return SVDResult(U, S, Vh)
    else:
        raise Exception(
            "1-dimensional array given. Array must be at least two-dimensional"
        )
