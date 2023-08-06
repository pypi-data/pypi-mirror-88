import glob
import logging
import os.path
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from src.output import FormattersRegistry
from src.output import IntFormatter
from src.output import PointFormatter
from src.output import PolynomialFormatter
from src.output import TaskConfigFormatter
from src.output import TaskResultFormatter
from src.parser.input_stream import metrics
from src.parser.input_stream import Parser


logger = logging.getLogger(__name__)

parser = Parser()
registry = FormattersRegistry()
int_formatter = IntFormatter()
polynomial_formatter = PolynomialFormatter(int_formatter)
point_formatter = PointFormatter(registry)
task_config_formatter = TaskConfigFormatter(
    point_formatter=point_formatter,
    int_formatter=int_formatter,
)
task_result_config = TaskResultFormatter(
    task_config_formatter=task_config_formatter,
    point_formatter=point_formatter,
)

registry.register(int_formatter)
registry.register(polynomial_formatter)
registry.register(point_formatter)
registry.register(task_config_formatter)
registry.register(task_result_config)


VERBOSE = False


def _get_most_common_base():
    return metrics.number_base.most_common()[0][0]


def _check_error(future: Future):
    if future.exception() is not None:
        if not VERBOSE:
            item = str(future.exception()).strip()
        else:
            item = future.exception()

        logger.error('Ошибка: %s', item)


def set_verbose(verbose: bool):
    global VERBOSE
    VERBOSE = verbose


def run(filename: str, dst_directory: str, base: Optional[int]):
    input_f = open(filename, 'r')
    filename = os.path.basename(filename)

    config = parser.parse(input_lines=iter(input_f))
    logger.info('Считал конфигурацию у файла %s. Начинаю построение таск раннера...', filename)
    task_runner = config.build_runner()
    formatter_context = {'base': base or _get_most_common_base()}
    logger.info(
        'В файле %s числа будут переведены в основание %d',
        filename, formatter_context['base'],
    )

    with open(os.path.join(dst_directory, filename), 'w') as output_f:
        logger.info('Таск раннер начал работу для файла %s', filename)

        for task_result in task_runner.run(config.task_configs):
            task_result_str = task_result_config.format(task_result, formatter_context)
            output_f.write(task_result_str + os.linesep)

    logger.info('Файл %s обработан; результаты записаны', filename)


def run_on_directory(src_directory: str, dst_directory: str, base: int):
    logger.info('Предварительные настройки')

    if not os.path.exists(dst_directory):
        try:
            os.mkdir(dst_directory)
            logger.info(
                'Создал выходную директорию %s',
                os.path.abspath(dst_directory),
            )
        except FileNotFoundError:
            logger.error('Ошибка: не удалось создать выходную директорию')
            return

    logger.info(
        'Запустилась обработка директории %s',
        os.path.abspath(src_directory),
    )

    with ThreadPoolExecutor() as executor:
        pattern = os.path.join(src_directory, '*.txt')

        for filename in glob.iglob(pattern):
            logger.info('Начал подсчет для файла %s', filename)
            future = executor.submit(run, filename, dst_directory, base)
            future.add_done_callback(_check_error)

    logger.info('Завершил работу со всеми файлами')
    logger.info(
        'Для просмотра результатов перейдите в каталог %s',
        os.path.abspath(dst_directory),
    )
