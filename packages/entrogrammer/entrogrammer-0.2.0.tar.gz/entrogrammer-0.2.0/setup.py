from setuptools import setup, find_packages
from entrogrammer import __version__

setup(
    name='entrogrammer',
    version=__version__,
    license='MIT',
    description='Entrogram calculator',
    author='J. Hariharan',
    author_email='jayaram.hariharan@utexas.edu',
    url='https://github.com/elbeejay/entrogrammer',
    packages=find_packages(exclude=['*.tests']),
    long_description='See: https://github.com/elbeejay/entrogrammer',
    classifiers=['Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8'],
    install_requires=['numpy', 'matplotlib', 'scipy', 'xarray', 'numba'],
)
