import setuptools
import numpy
import os

with open("README.md", "r") as f:
    long_description = f.read()

_mli_path = os.path.join(
    "homogeneous_transformation",
    "_merlict_c89_wrapper",
    "merlict_c89",
    "merlict_c89",
)

setuptools.setup(
    name="homogeneous_transformation",
    version="0.0.0",
    author="Sebastian Achim Mueller",
    author_email="sebastianachimmueller@gmail.com",
    description="Transform positions and directions in between 3D frames.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cherenkov-plenoscope/homogeneous_transformation",
    packages=[
        "homogeneous_transformation",
        "homogeneous_transformation._merlict_c89_wrapper",
    ],
    install_requires=["setuptools>=18.0", "cython",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3",
    ext_modules=[
        setuptools.Extension(
            "homogeneous_transformation._merlict_c89_wrapper.wrapper",
            sources=[
                os.path.join(
                    "homogeneous_transformation",
                    "_merlict_c89_wrapper",
                    "wrapper.pyx",
                ),
                os.path.join(_mli_path, "mliVec.c"),
                os.path.join(_mli_path, "mliRay.c"),
                os.path.join(_mli_path, "mliRotMat.c"),
                os.path.join(_mli_path, "mliQuaternion.c"),
                os.path.join(_mli_path, "mliHomTra.c"),
            ],
            include_dirs=[numpy.get_include(), "homogeneous_transformation"],
            language="c",
        ),
    ],
)
