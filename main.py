import argparse

from lib.SVD.SVD import SVD
from lib.classes import ArgError
from lib.consts import (
    BMP_METADATA_SIZE,
    CHANNELS,
    FLOAT32_SIZE,
    METADATA_SIZE,
    Method,
    Mode,
)
from lib.utils import image_to_matrix, postreshape, prereshape
from lib.compress import compress
from lib.decompress import decompress
from PIL import Image


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        type=str,
        help=f'"{Mode.COMPRESS}" or "{Mode.DECOMPRESS}"',
        required=True,
    )
    parser.add_argument(
        "--method",
        type=str,
        help=f'"{Method.NUMPY}", "{Method.SIMPLE}" or "{Method.ADVANCED}"',
    )
    parser.add_argument("--compression", type=float, help="Image compression ratio")
    parser.add_argument("--path", type=str, help="Path to image to compress")
    parser.add_argument(
        "--binpath", type=str, help="Path to compression result", default="out.bin"
    )
    parser.add_argument(
        "--bmppath", type=str, help="Path to decompression result", default="out.bmp"
    )

    args = parser.parse_args()
    match args.mode:
        case Mode.COMPRESS:
            N = args.compression
            if N is None:
                raise ArgError("compression")
            matrix = prereshape(image_to_matrix(args.path))
            _, m, n = matrix.shape
            r = min(
                int(
                    (CHANNELS * m * n + BMP_METADATA_SIZE - N * METADATA_SIZE)
                    / (FLOAT32_SIZE * CHANNELS * N * (m + n + 1))
                ),
                m,
                n,
            )
            svd_result = SVD(matrix, r, args.method)
            compress(svd_result, args.binpath, m, n, r)
        case Mode.DECOMPRESS:
            compressed = args.binpath
            matrix_of_image = decompress(compressed)
            img = Image.fromarray(postreshape(matrix_of_image), "RGB")
            img.save(args.bmppath)
        case _:
            raise ArgError("mode")


if __name__ == "__main__":
    main()
