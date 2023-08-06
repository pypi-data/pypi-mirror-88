"""  Setup script. Used by easy_install and pip. """

import os
import sys
import re
import numpy
from setuptools import setup, find_packages, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    # create closure for deferred import
    def cythonize(*args, **kwargs):
        from Cython.build import cythonize
        return cythonize(*args, **kwargs)

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

"""Discover the package version"""
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
VERSIONFILE = "mdplus/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RunTimeError("Unable to find version string in {}.".format(VERSIONFILE))


"""Check Python version"""
if  sys.version_info[0:2] < (3, 4):
    raise RuntimeError('mdplus requires Python 3.4+')

setup_args = {
    'name':             "mdplus",
    'version':          verstr,
    'description':      "Tools for molecular dynamics simulation setup and analysis.",
    'long_description_content_type':      "text/markdown",
    'long_description':      read('README.md'),
    'author':           "The University of Nottingham & BSC",
    'author_email':     "charles.laughton@nottingham.ac.uk",
    'url':              "https://bitbucket.org/claughton/mdplus/overview",
    'download_url':     "https://bitbucket.org/claughton/mdplus/get/{}.tar.gz".format(verstr),
    'license':          "BSD license.",

    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],

    'packages': find_packages(),

    'install_requires': ['numpy',
                         'scipy',
                         'Cython',
                         'scikit-learn',
                         'mdtraj',
                         ],

    'zip_safe': False,
    'ext_modules': cythonize(Extension(
                       name='mdplus.fast',
                       sources=['mdplus/fast/make_dx.pyx'],
                       include_dirs=[numpy.get_include()]))
}

setup(**setup_args)
