import setuptools
import numpy
import os


with open("README.md", "r") as f:
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
    name="homogeneous_transformation_sebastian_achim_mueller",
    version=version,
    description="View and work on plenoscope events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cherenkov-plenoscope/plenopy.git",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    license="MIT",
    packages=["homogeneous_transformation"],
    package_data={"homogeneous_transformation": []},
    install_requires=["setuptools>=18.0", "cython",],
    zip_safe=False,
    ext_modules=[
        setuptools.Extension(
            "homogeneous_transformation.merlict_c89.wrapper",
            sources=[
                os.path.join(
                    "homogeneous_transformation", "merlict_c89", "wrapper.pyx"
                ),
                os.path.join(
                    "homogeneous_transformation", "merlict_c89", "mli_subset.c"
                ),
            ],
            include_dirs=[
                numpy.get_include(),
                os.path.join("homogeneous_transformation", "merlict_c89"),
            ],
            language="c",
        ),
    ],
)
