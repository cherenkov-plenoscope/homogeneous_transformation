import numpy as np
from collections import namedtuple
cimport cython

cdef extern from "merlict_c89/merlict_c89/mliVec.h":
    struct mliVec:
        double x
        double y
        double z

    mliVec mliVec_set(
        const double x,
        const double y,
        const double z
    )

cdef extern from "merlict_c89/merlict_c89/mliRay.h":
    struct mliRay:
        pass


cdef extern from "merlict_c89/merlict_c89/mliRotMat.h":
    struct mliRotMat:
        pass


cdef extern from "merlict_c89/merlict_c89/mliQuaternion.h":
    struct mliQuaternion:
        double w
        double x
        double y
        double z

    mliQuaternion mliQuaternion_set(
        const double w,
        const double x,
        const double y,
        const double z
    )

    mliQuaternion mliQuaternion_set_unit_xyz(
        const double x,
        const double y,
        const double z
    )

    mliQuaternion mliQuaternion_set_tait_bryan(
        const double rx,
        const double ry,
        const double rz
    )

    mliQuaternion mliQuaternion_set_rotaxis_and_angle(
        const mliVec rot_axis,
        const double angle
    )


cdef extern from "merlict_c89/merlict_c89/mliHomTra.h":
    struct mliHomTra:
        pass

    struct mliHomTraComp:
        mliVec trans
        mliQuaternion rot

    mliHomTraComp mliHomTraComp_set(
        const mliVec trans,
        const mliQuaternion rot
    )

    mliHomTraComp mliHomTraComp_sequence(
        const mliHomTraComp a,
        const mliHomTraComp b
    )

    mliHomTra mliHomTra_from_compact(const mliHomTraComp trafo)

    mliVec mliHomTra_pos(const mliHomTra *t, const mliVec i)
    mliVec mliHomTra_pos_inverse(const mliHomTra *t, const mliVec i)
    mliVec mliHomTra_dir(const mliHomTra *t, const mliVec i)
    mliVec mliHomTra_dir_inverse(const mliHomTra *t, const mliVec i)


Quaternion = namedtuple('Quaternion', ['w', 'x', 'y', 'z'])
HomTra = namedtuple('HomTra', ['trans', 'rot'])
Vec = namedtuple('Vec', ['x', 'y', 'z'])

def Quaternion_set_tait_bryan(x, y, z):
    q = mliQuaternion_set_tait_bryan(x, y, z)
    return Quaternion(q.w, q.x, q.y, q.z)


def Quaternion_set_rotaxis_and_angle(rot_axis, angle):
    q = mliQuaternion_set_rotaxis_and_angle(
        mliVec_set(rot_axis[0], rot_axis[1], rot_axis[2]),
        angle
    )
    return Quaternion(q.w, q.x, q.y, q.z)


def Quaternion_set_unit_xyz(x, y, z):
    q = mliQuaternion_set_unit_xyz(x, y, z)
    return Quaternion(q.w, q.x, q.y, q.z)


def sequence(a, b):
    _a = mliHomTraComp_set(
        mliVec_set(a.trans.x, a.trans.y, a.trans.z),
        mliQuaternion_set(a.rot.w, a.rot.x, a.rot.y, a.rot.z)
    )
    _b = mliHomTraComp_set(
        mliVec_set(b.trans.x, b.trans.y, b.trans.z),
        mliQuaternion_set(b.rot.w, b.rot.x, b.rot.y, b.rot.z)
    )
    _c = mliHomTraComp_sequence(_a, _b)
    return HomTra(
        Quaternion(_c.rot.w, _c.rot.x, _c.rot.y, _c.rot.z),
        Vec(_c.trans.x, _c.trans.y, _c.trans.z)
    )


cdef mliHomTra _extract_homtra(homtra):
    H_comp = mliHomTraComp_set(
        mliVec_set(
            homtra.trans.x,
            homtra.trans.y,
            homtra.trans.z
        ),
        mliQuaternion_set(
            homtra.rot.w,
            homtra.rot.x,
            homtra.rot.y,
            homtra.rot.z,
        )
    )
    H = mliHomTra_from_compact(H_comp)
    return H


def transform_position(homtra, position):
    H = _extract_homtra(homtra)
    v = mliHomTra_pos(
        &H,
        mliVec_set(position[0], position[1], position[2])
    )
    return [v.x, v.y, v.z]


def transform_position_inverse(homtra, position):
    H = _extract_homtra(homtra)
    v = mliHomTra_pos_inverse(
        &H,
        mliVec_set(position[0], position[1], position[2])
    )
    return [v.x, v.y, v.z]


def transform_direction(homtra, direction):
    H = _extract_homtra(homtra)
    v = mliHomTra_dir(
        &H,
        mliVec_set(direction[0], direction[1], direction[2])
    )
    return [v.x, v.y, v.z]


def transform_direction_inverse(homtra, direction):
    H = _extract_homtra(homtra)
    v = mliHomTra_dir_inverse(
        &H,
        mliVec_set(direction[0], direction[1], direction[2])
    )
    return [v.x, v.y, v.z]
