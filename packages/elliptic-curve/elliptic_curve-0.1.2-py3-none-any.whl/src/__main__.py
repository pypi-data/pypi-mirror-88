from argparse import ArgumentParser

from src.app import run_on_directory
from src.app import set_verbose
from src.settings import setup_logging


arg_parse = ArgumentParser(
    description=(
        'Скрипт для сложения точек эллиптической кривой. '
        'Подробно о формате входных файлов смотреть в документацию. '
        'Документация находится в репозитории проекта в README.md'
    ),
)
arg_parse.add_argument(
    '-s', '--src',
    default='input',
    help='Входная директория',
)
arg_parse.add_argument(
    '-d', '--dst',
    default='output',
    help='Выходная директория',
)
arg_parse.add_argument(
    '--base',
    help='Основание системы счисления выходных файлов. Доступные: 2, 8, 10, 16',
    type=int,
    default=None,
)
arg_parse.add_argument(
    '-v', '--verbose',
    action='store_true',
    help='Включает более подробный вывод',
)


def main():
    setup_logging()
    options = arg_parse.parse_args()
    set_verbose(options.verbose)
    run_on_directory(
        src_directory=options.src,
        dst_directory=options.dst,
        base=options.base,
    )


if __name__ == '__main__':
    main()
