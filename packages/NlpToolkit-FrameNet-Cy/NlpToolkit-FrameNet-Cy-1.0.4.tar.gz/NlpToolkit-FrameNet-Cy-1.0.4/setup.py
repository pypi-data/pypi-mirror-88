from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["FrameNet/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-FrameNet-Cy',
    version='1.0.4',
    packages=['FrameNet'],
    package_data={'FrameNet': ['*.pxd', '*.pyx', '*.c', '*.py']},
    url='https://github.com/StarlangSoftware/TurkishFrameNet-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='FrameNet library'
)
