import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='csv_etl',
    packages=find_packages(include=['csv_etl']),
    version='0.0.2',
    description='',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/winslowdibona/csv_etl",
    author='Winslow DiBona',
    license='MIT',
    install_requires=['pyyaml'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
