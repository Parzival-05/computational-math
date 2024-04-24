from typing import Iterable
import numpy
from numpy.linalg.linalg import SVDResult


from lib.consts import INT_SIZE
from lib.utils import create_file, write_bytes


def crop_3dmatrix(matrix: numpy.ndarray, h: int, w: int) -> numpy.ndarray:
    return matrix[:, 0:h, 0:w]


def array_to_bytes(a: Iterable, size: int) -> bytes:
    return b"".join(
        map(
            lambda x: x.to_bytes(
                size,
            ),
            a,
        )
    )


def matrix_to_bytes(matrix: numpy.ndarray) -> bytes:
    return matrix.astype(numpy.float32).tobytes()


def compress(svd_result: SVDResult, out: str, m: int, n: int, r: int):
    create_file(out)
    header_bytes = array_to_bytes([m, n, r], INT_SIZE)

    U_compressed = crop_3dmatrix(svd_result.U, m, r)
    S_compressed = svd_result.S[:, 0:r]
    V_compressed = crop_3dmatrix(svd_result.Vh, r, n)

    U_bytes = matrix_to_bytes(U_compressed)
    S_bytes = matrix_to_bytes(S_compressed)
    V_bytes = matrix_to_bytes(V_compressed)

    write_bytes(out, header_bytes)
    write_bytes(out, U_bytes)
    write_bytes(out, S_bytes)
    write_bytes(out, V_bytes)
