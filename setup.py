"""Compiles pyx files"""
import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

os.chdir('rogue/')

EXT_MODULES = [
    Extension("render.render", ["render/render.pyx"],
              libraries=['bearlibterminal'],
              library_dirs=["../BearLibTerminal_0.15.7/Windows32", numpy.get_include()]),
    Extension("control.control", ["control/control.pyx"],
              libraries=['bearlibterminal'],
              library_dirs=["../BearLibTerminal_0.15.7/Windows32"]),
    Extension("fps.fps", ["fps/fps.pyx"]),
    Extension("los.los", ["los/los.pyx"]),
]

setup(
    name='Rogue',
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(EXT_MODULES, 
                          build_dir="build", 
                          compiler_directives={'language_level' : '3'}),
    package_dir={"": ""},
    include_dirs=["../BearLibTerminal_0.15.7/Include/C", numpy.get_include()]
)
