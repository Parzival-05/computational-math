from PIL import Image
import numpy


def image_to_matrix(image: str) -> numpy.ndarray:
    try:
        img = Image.open(image)
    except:
        raise Exception("Invalid image path")
    matrix = numpy.asarray(img)
    return matrix


def prereshape(matrix: numpy.ndarray):
    shape = matrix.shape
    reshaped = numpy.reshape(matrix, (shape[2], shape[0], shape[1]))
    return reshaped


def postreshape(matrix: numpy.ndarray):
    shape = matrix.shape
    reshaped = numpy.reshape(matrix, (shape[1], shape[2], shape[0]))
    return reshaped


def create_file(file: str):
    with open(file, "w") as _:
        pass
    return


def write_bytes(file: str, bytes: bytes):
    with open(file, "ab") as f:
        f.write(bytes)
