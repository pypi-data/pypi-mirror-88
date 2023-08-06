import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages
from setuptools import setup

project_name = 'elliptic-curve'
module_name = 'src'

module = SourceFileLoader(
    fullname=module_name,
    path=os.path.join(module_name, '__init__.py'),
).load_module()


def load_requirements(*filenames: str) -> list:
    for filename in filenames:
        with open(filename, 'r') as fp:
            requirements_lines = fp.readlines()
            requirements_lines = filter(
                lambda s: not s.strip().startswith('-r'),
                requirements_lines,
            )

            for req in parse_requirements(requirements_lines):
                extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
                yield '{}{}{}'.format(req.name, extras, req.specifier)


setup(
    name=project_name,
    version='0.1.2',
    author='d4n13lzh3',
    author_email='zhe.dan28@gmail.com',
    description='Учебный проект для сложения точек эллиптической кривой',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    platforms='all',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.7',
    packages=find_packages(exclude=['tests']),
    extras_require={
        'dev': list(
            load_requirements(
                'requirements-dev.txt',
                'requirements-test.txt',
            ),
        ),
    },
    entry_points={
        'console_scripts': [
            '{0} = src.__main__:main'.format(project_name),
        ],
    },
    include_package_data=True,
)
