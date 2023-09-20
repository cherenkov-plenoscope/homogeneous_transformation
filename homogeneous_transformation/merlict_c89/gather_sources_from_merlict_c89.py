"""
This script is only executed to either gather the c-sources from merlict_c89,
or to bumb the version-number.
"""
import os
import sys
import shutil

merlict_c89_dir = sys.argv[1]
homogeneous_transformation_dir = sys.argv[2]

src = os.path.join(merlict_c89_dir, "merlict")
dst = os.path.join(
    homogeneous_transformation_dir, "homogeneous_transformation", "merlict_c89"
)

parts = [
    "chk_debug",
    "mli_version",
    "mliVec",
    "mliQuaternion",
    "mliHomTra",
    "mliRay",
    "mliMat",
    "mli_quadratic_equation",
]

for p in parts:
    shutil.copy(os.path.join(src, "{:s}.h".format(p)), dst)
    shutil.copy(os.path.join(src, "{:s}.c".format(p)), dst)


# gather merlict version
# ----------------------
MERLICT_C89_VERSION = {
    "MAYOR": -1,
    "MINOR": -1,
    "PATCH": -1,
}
MERLICT_C89_VERSION_DIGIT_POS = len("#define MLI_VERSION_MAYOR ")

with open(os.path.join(dst, "mli_version.h"), "rt") as f:
    txt = f.read()
    keys = list(MERLICT_C89_VERSION.keys())
    for line in str.splitlines(txt):
        for key in keys:
            if key in line:
                MERLICT_C89_VERSION[key] = int(
                    line[MERLICT_C89_VERSION_DIGIT_POS:]
                )

MERLICT_C89_VERSION_STR = "{:d}.{:d}.{:d}".format(
    MERLICT_C89_VERSION["MAYOR"],
    MERLICT_C89_VERSION["MINOR"],
    MERLICT_C89_VERSION["PATCH"],
)

# define this py-package's version
# --------------------------------
homogeneous_transformation_VERSION_STR = "0.0.1"

# combine versions
# ----------------
VERSION_STR = "{:s}.{:s}".format(
    homogeneous_transformation_VERSION_STR,
    MERLICT_C89_VERSION_STR,
)

# export version
# --------------
version_path = os.path.join(
    homogeneous_transformation_dir,
    "homogeneous_transformation",
    "version.py",
)
with open(os.path.join(version_path), "wt") as f:
    f.write("# I was written by: ")
    f.write("merlict_c89/gather_sources_from_merlict_c89.py\n")
    f.write('__version__ = "' + VERSION_STR + '"\n')
