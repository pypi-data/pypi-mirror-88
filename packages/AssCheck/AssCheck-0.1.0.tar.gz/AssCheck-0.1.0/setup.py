from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = ( HERE / "README.md").read_text() 
setup(
    name='AssCheck',
    packages=find_packages(),
    version='0.1.0',
    description='check basic python exercises with pretty feedback',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/QUBAMA1021/test_utils",
    author='Andrew Brown',
    license='MIT',
)
