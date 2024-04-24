import numpy
from lib.classes import SVDResult
from lib.consts import FLOAT32_SIZE, INT_SIZE, CHANNELS


def read_int_value(file) -> int:
    return int.from_bytes(file.read(INT_SIZE))


def read_matrix(file, h: int, w: int) -> numpy.ndarray:
    flatten = numpy.frombuffer(
        file.read(FLOAT32_SIZE * CHANNELS * h * w), dtype=numpy.float32
    )
    return numpy.reshape(flatten, (CHANNELS, h, w))


def read_svd_result(file: str) -> SVDResult:
    with open(file, "rb") as f:
        m = read_int_value(f)
        n = read_int_value(f)
        r = read_int_value(f)

        U = read_matrix(f, m, r)
        S = read_matrix(f, 1, r)
        V = read_matrix(f, r, n)
    return SVDResult(U, S, V)


def recover(svd_result: SVDResult) -> numpy.ndarray:
    recovered_matrix = numpy.rint(
        svd_result.U
        @ numpy.array(list(map(numpy.diagflat, svd_result.S)))
        @ svd_result.Vh
    ).astype(numpy.ubyte)
    return recovered_matrix


def decompress(compressed: str) -> numpy.ndarray:
    svd_result = read_svd_result(compressed)
    recovered_matrix = recover(svd_result)
    return recovered_matrix
