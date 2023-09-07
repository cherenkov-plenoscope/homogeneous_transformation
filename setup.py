import setuptools
import os
from Cython.Build import cythonize


with open("README.rst", "r") as f:
    long_description = f.read()


version_path = os.path.join(
    "homogeneous_transformation", "automatically_generated_version.py"
)
with open(version_path, "r") as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")


setuptools.setup(
    name="homogeneous_transformation_sebastian-achim-mueller",
    version=version,
    description="View and work on plenoscope events",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/homogeneous_transformation.git",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=[
        "homogeneous_transformation",
        "homogeneous_transformation.merlict_c89",
    ],
    package_data={"homogeneous_transformation": [],},
    install_requires=["setuptools>=18.0", "cython",],
    ext_modules=cythonize(
        os.path.join("homogeneous_transformation", "merlict_c89", "*.pyx"),
        include_path=[
            os.path.join("homogeneous_transformation", "merlict_c89"),
        ],
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
)
