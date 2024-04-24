from numpy import float32


INT_SIZE = 4
FLOAT32_SIZE = 4
CHANNELS = 3
METADATA_SIZE = 3 * INT_SIZE
BMP_METADATA_SIZE = 54


class Mode:
    COMPRESS = "compress"
    DECOMPRESS = "decompress"


class Method:
    NUMPY = "numpy"
    SIMPLE = "simple"
    ADVANCED = "advanced"
