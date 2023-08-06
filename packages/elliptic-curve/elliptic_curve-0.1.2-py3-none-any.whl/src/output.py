from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Generic
from typing import get_args
from typing import Type
from typing import TypeVar

from src.elliptic.elliptic import Point
from src.polynomial.polynomial import Polynomial
from src.task import TaskConfig
from src.task import TaskResult
from src.task import TaskType


T = TypeVar('T')


def _get_generic_type(instance: Any):
    instance_cls = instance.__class__
    generic_type = get_args(instance_cls.__orig_bases__[0])[0]

    return generic_type


class Formatter(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def format(self, item: T, context: Dict[str, Any]) -> str:
        raise NotImplementedError


class FormattersRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, formatter: Formatter):
        generic_type = _get_generic_type(formatter)
        self._registry[generic_type] = formatter

    def get(self, type_: Type):
        try:
            return self._registry[type_]
        except KeyError:
            raise ValueError(f'Форматтер для данного типа {type_} не зарегистрирован')


class IntFormatter(Formatter[int]):
    _formats = {
        2: '0b{0:b}',
        8: '0o{0:o}',
        10: '{0:d}',
        16: '0x{0:x}',
    }

    def __init__(self, default_base: int = 10):
        self._default_base = default_base
        self._check_default_format(default_base)

    def format(self, item: int, context: Dict[str, Any]) -> str:
        base = context.get('base', self._default_base)
        format_string = self._formats.get(base, self._formats[self._default_base])

        return format_string.format(item)

    @classmethod
    def _check_default_format(cls, base: int):
        try:
            cls._formats[base]
        except KeyError:
            raise ValueError('Формат для данного основания не определен')


class PolynomialFormatter(Formatter[Polynomial]):
    def __init__(self, int_formatter: IntFormatter):
        self._int_formatter = int_formatter

    def format(self, item: Polynomial, context: Dict[str, Any]) -> str:
        return self._int_formatter.format(
            item=item.bits,
            context=context,
        )


class PointFormatter(Formatter[Point]):
    def __init__(self, formatters_registry: FormattersRegistry):
        self._registry = formatters_registry

    def format(self, item: Point, context: Dict[str, Any]) -> str:
        if item.is_infinite():
            return 'O'

        formatter = self._registry.get(type(item.x))
        x_str = formatter.format(item.x, context)
        y_str = formatter.format(item.y, context)

        return f'({x_str}, {y_str})'


class TaskConfigFormatter(Formatter[TaskConfig]):
    def __init__(
        self,
        point_formatter: PointFormatter,
        int_formatter: IntFormatter,
    ):
        self._point_formatter = point_formatter
        self._int_formatter = int_formatter

    def format(self, item: TaskConfig, context: Dict[str, Any]) -> str:
        if item.task_type is TaskType.MUL:
            point = self._point_formatter.format(item.points[0], context)
            scalar = self._int_formatter.format(item.scalar, context)
            return f'{scalar} * {point}'

        if item.task_type is TaskType.ADD:
            points = [
                self._point_formatter.format(point, context)
                for point in item.points
            ]
            return ' + '.join(points)

        raise ValueError(f'Не умею выводить выводить операцию: {item.task_type}')


class TaskResultFormatter(Formatter[TaskResult]):
    def __init__(
        self,
        task_config_formatter: TaskConfigFormatter,
        point_formatter: PointFormatter,
    ):
        self._task_config_formatter = task_config_formatter
        self._point_formatter = point_formatter

    def format(self, item: TaskResult, context: Dict[str, Any]) -> str:
        task_config_str = self._task_config_formatter.format(item.task_config, context)
        result = self._point_formatter.format(item.result, context)

        return f'{task_config_str} = {result}'
