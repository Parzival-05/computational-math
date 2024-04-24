class SVDResult:
    def __init__(self, U, S, Vh):
        self.U = U
        self.S = S
        self.Vh = Vh


class ArgError(Exception):
    def __init__(self, arg: str):
        self.txt = f'Please specify the "{arg}" parameter'
