from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("Preprocessor", ["Preprocessor.pyx"],
        include_dirs=[],
        libraries=['opencv_imgcodecs', 'opencv_imgproc',],
        library_dirs=[],
    	extra_compile_args=['-std=c++11'])
]
setup(
    ext_modules=cythonize(extensions),
)

'''
extensions = [
    Extension("Predictor", ["Predictor.pyx"],
        include_dirs=[],
        libraries=["-fopenmp"],
        library_dirs=[]),
]

setup(
    name="Predictor",
    ext_modules=cythonize(extensions),
)
'''