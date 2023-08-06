class ParserError(Exception):
    pass


class PolynomialParseError(ParserError):
    def __init__(self, monomial_raw: str, polynomial_raw: str):
        super().__init__(f'Ошибка при парсинге одночлена: {monomial_raw} (полином: {polynomial_raw})')
