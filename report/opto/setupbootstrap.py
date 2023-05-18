import os
from pathlib import Path
from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy

# setup(
#     # python setup.py build_ext --inplace
#     ext_modules=cythonize("bootstrap.pyx"),
#     package_dir={f"{Path(os.getcwd()).name}": ''},
#     include_dirs=[numpy.get_include()]
# )

ext_modules = [
    Extension(
        "bootstrap",
        ["bootstrap.pyx"],
        extra_compile_args=['/openmp'],
        extra_link_args=['/fopenmp'],
    )
]

setup(
    name='bootstrap',
    package_dir={f"{Path(os.getcwd()).name}": ''},
    include_dirs=[numpy.get_include()],
    ext_modules=cythonize(ext_modules),
)
