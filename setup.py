import setuptools
import os
import Cython
from Cython import Build
import numpy


with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()


with open(os.path.join("homogeneous_transformation", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")


merlict_c89_sources = [
    "chk_debug.c",
    "mli_quadratic_equation.c",
    "mli_version.c",
    "mliHomTra.c",
    "mliMat.c",
    "mliQuaternion.c",
    "mliRay.c",
    "mliVec.c",
]

extensions = [
    setuptools.Extension(
        name="homogeneous_transformation.merlict_c89.wrapper",
        sources=[
            os.path.join(
                "homogeneous_transformation", "merlict_c89", "wrapper.pyx"
            ),
        ]
        + [
            os.path.join("homogeneous_transformation", "merlict_c89", pp)
            for pp in merlict_c89_sources
        ],
        include_dirs=[numpy.get_include()],
    )
]

setuptools.setup(
    name="homogeneous_transformation",
    version=version,
    description="View and work on plenoscope events",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/homogeneous_transformation",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=[
        "homogeneous_transformation",
        "homogeneous_transformation.merlict_c89",
    ],
    package_data={
        "homogeneous_transformation": [
            os.path.join("merlict_c89", "*"),
        ],
    },
    install_requires=[],
    ext_modules=Cython.Build.cythonize(extensions),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
)
