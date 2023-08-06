from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic
from typing import Optional
from typing import Type
from typing import TypeVar

from src.elliptic.errors import CalculationError
from src.elliptic.errors import InfinitePoint
from src.field import Field
from src.field import GF2PolynomialField
from src.field import ZpField
from src.polynomial.polynomial import Polynomial


T = TypeVar('T')


@dataclass(unsafe_hash=True)
class Point(Generic[T]):
    x: Optional[T]
    y: Optional[T]

    @classmethod
    def infinity(cls):
        return cls(x=None, y=None)

    def is_infinite(self):
        return self.x is None and self.y is None


class Curve(Generic[T], metaclass=ABCMeta):
    def __init__(self, field_order: T, field_cls: Type[Field[T]]):
        self._field: Field[T] = field_cls(field_order)

    def add(self, first_point: Point[T], second_point: Point[T]) -> Point[T]:
        if first_point.is_infinite():
            return second_point

        if second_point.is_infinite():
            return first_point

        try:
            if first_point.x != second_point.x:
                k = self._first_case_coefficient(first_point, second_point)
            elif (
                first_point.x == second_point.x and
                first_point.y != second_point.y
            ):
                k = self._second_case_coefficient(first_point, second_point)
            else:
                k = self._third_case_coefficient(first_point, second_point)
        except InfinitePoint:
            return Point.infinity()

        k = self._field.normalize_element(k)
        result_point = self._additive_point(first_point, second_point, coefficient=k)
        result_point.x = self._field.normalize_element(result_point.x)
        result_point.y = self._field.normalize_element(result_point.y)

        return result_point

    def mul(self, first_point: Point[T], scalar: int) -> Point[T]:
        result = Point.infinity()
        addend = first_point

        while scalar:
            if scalar & 1:
                result = self.add(result, addend)

            addend = self.add(addend, addend)

            scalar >>= 1

        return result

    @abstractmethod
    def _first_case_coefficient(self, first_point: Point[T], second_point: Point[T]) -> T:
        """Считает коэффициент для первого случая в случае если x1 == x2
        """
        raise NotImplementedError

    @abstractmethod
    def _second_case_coefficient(self, first_point: Point[T], second_point: Point[T]) -> T:
        """Считает коэффициент для первого случая в случае если x1 != x2 && y1 == y2
        """
        raise NotImplementedError

    @abstractmethod
    def _third_case_coefficient(self, first_point: Point[T], second_point: Point[T]) -> T:
        """Считает коэффициент для первого случая в случае если точки равны
            """
        raise NotImplementedError

    @abstractmethod
    def _additive_point(
        self,
        first_point: Point[T],
        second_point: Point[T],
        coefficient: T,
    ) -> Point[T]:
        """Считает итоговую точку процесса "сложения" двух точек эллиптической кривой
        """
        raise NotImplementedError


class ZpCurve(Curve[int]):
    def __init__(self, p: int, a: int, b: int):
        self._a = a
        self._b = b
        super().__init__(p, field_cls=ZpField)

    def _first_case_coefficient(self, first_point: Point[int], second_point: Point[int]) -> int:
        return self._field.modulus(
            (second_point.y - first_point.y) *
            self._field.invert(second_point.x - first_point.x),
        )

    def _second_case_coefficient(self, first_point: Point[int], second_point: Point[int]) -> int:  # noqa
        if self._field.modulus(first_point.y + second_point.y) == self._field.zero():
            raise InfinitePoint

        raise ValueError(f'{self.__class__.__name__}: Невозможные условия для 2-го случая')

    def _third_case_coefficient(self, first_point: Point[int], second_point: Point[int]) -> int:
        return self._field.modulus(
            (3 * first_point.x ** 2 + self._a) *
            self._field.invert(2 * first_point.y),
        )

    def _additive_point(
        self,
        first_point: Point[int],
        second_point: Point[int],
        coefficient: int,
    ) -> Point[int]:
        x3 = self._field.modulus(coefficient ** 2 - first_point.x - second_point.x)
        y3 = self._field.modulus(first_point.y + coefficient * (x3 - first_point.x))

        return Point(x3, self._field.modulus(-y3))


class GF2CurveBase(Curve[Polynomial], metaclass=ABCMeta):
    def __init__(self, p: Polynomial, a: Polynomial, b: Polynomial, c: Polynomial):
        self._a = a
        self._b = b
        self._c = c
        super().__init__(field_order=p, field_cls=GF2PolynomialField)


class GF2NotSupersingularCurve(GF2CurveBase):
    def _first_case_coefficient(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
    ) -> Polynomial:
        return self._field.modulus(
            (first_point.y + second_point.y) *
            self._field.invert(first_point.x + second_point.x),
        )

    def _second_case_coefficient(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
    ) -> Polynomial:  # noqa
        if self._field.modulus(second_point.y) == self._field.modulus(self._a * first_point.x + first_point.y):
            raise InfinitePoint

        raise CalculationError(f'{self.__class__.__name__}: Я не знаю как считать 2 случай')

    def _third_case_coefficient(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
    ) -> Polynomial:
        return self._field.modulus(
            (first_point.x * first_point.x + self._a * first_point.y) *
            self._field.invert((self._a * first_point.x)),
        )

    def _additive_point(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
        coefficient: Polynomial,
    ) -> Point[Polynomial]:
        x3 = self._field.modulus(
            coefficient * coefficient + self._a * coefficient +
            self._b + first_point.x + second_point.x,
        )
        y3 = self._field.modulus(first_point.y + coefficient * (x3 + first_point.x))

        return Point(x3, self._field.modulus(self._a * x3 + y3))


class GF2SupersingularCurve(GF2CurveBase):
    def _first_case_coefficient(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
    ) -> Polynomial:
        return self._field.modulus(
            (first_point.y + second_point.y) *
            self._field.invert(first_point.x + second_point.x),
        )

    def _second_case_coefficient(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
    ) -> Polynomial:  # noqa
        if self._field.modulus(second_point.y) == self._field.modulus(self._a + first_point.y):
            raise InfinitePoint

        raise CalculationError(f'{self.__class__.__name__}: Я не знаю как считать 2 случай')

    def _third_case_coefficient(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
    ) -> Polynomial:
        if self._field.modulus(self._a) == self._field.zero():
            raise CalculationError('Коэффиициент a не может быть 0')

        return self._field.modulus(
            (first_point.x * first_point.x + self._b) *
            self._field.invert(self._a),
        )

    def _additive_point(
        self,
        first_point: Point[Polynomial],
        second_point: Point[Polynomial],
        coefficient: Polynomial,
    ) -> Point[Polynomial]:
        x3 = self._field.modulus(
            coefficient * coefficient + first_point.x + second_point.x,
        )
        y3 = self._field.modulus(first_point.y + coefficient * (x3 + first_point.x))

        return Point(x3, self._field.modulus(self._a + y3))
