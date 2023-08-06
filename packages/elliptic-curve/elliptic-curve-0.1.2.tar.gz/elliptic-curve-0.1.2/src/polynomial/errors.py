class PolynomialException(Exception):
    pass


class UnknownIrreduciblePolynomialPower(PolynomialException):
    def __init__(self, power: int):
        super().__init__(f'Я не знаю неприводимого полинома степени {power=} над GF(2^power)')
