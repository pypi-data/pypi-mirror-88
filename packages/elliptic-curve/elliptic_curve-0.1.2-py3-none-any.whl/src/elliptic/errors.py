class EllipticCurveError(Exception):
    pass


class InfinitePoint(EllipticCurveError):
    pass


class CalculationError(EllipticCurveError):
    pass
