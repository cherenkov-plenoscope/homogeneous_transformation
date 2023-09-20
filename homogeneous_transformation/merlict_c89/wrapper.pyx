import numpy as np
cimport numpy as cnp
cnp.import_array()


cdef extern from "mliVec.h":
    cdef struct mliVec:
        double x
        double y
        double z


cdef extern from "mliRay.h":
    cdef struct mliRay:
        mliVec support
        mliVec direction


cdef extern from "mliQuaternion.h":
    cdef struct mliQuaternion:
        double w
        double x
        double y
        double z

    double mliQuaternion_norm(mliQuaternion q)

    mliQuaternion mliQuaternion_set_tait_bryan (
        const double rx,
        const double ry,
        const double rz,
    )

    mliQuaternion mliQuaternion_set_rotaxis_and_angle(
        const mliVec rot_axis,
        const double angle,
    )

    mliQuaternion mliQuaternion_set_unit_xyz(
        const double x,
        const double y,
        const double z,
    )

    mliMat mliQuaternion_to_matrix(const mliQuaternion quat)


cdef extern from "mliHomTra.h":
    cdef struct mliHomTraComp:
        mliVec translation
        mliQuaternion rotation

    mliHomTraComp mliHomTraComp_sequence(
        const mliHomTraComp a,
        const mliHomTraComp b,
    )


cdef extern from "mliMat.h":
    cdef struct mliMat:
        double r00
        double r01
        double r02
        double r10
        double r11
        double r12
        double r20
        double r21
        double r22


cdef extern from "loops.h":
    int mliHomTraComp_transform(
        const mliHomTraComp t_comp,
        const double* vec_in,
        double* vec_out,
        unsigned long num_vec,
        const unsigned long mode,
    )


def _mliVec2py(mliVec mliv):
    return np.array([mliv.x, mliv.y, mliv.z], dtype=np.float64)


def _mliVec(v):
    cdef mliVec mliv
    mliv.x = v[0]
    mliv.y = v[1]
    mliv.z = v[2]
    return mliv


def _mliQuaternion2py(mliQuaternion mliq):
    return np.array([mliq.w, mliq.x, mliq.y, mliq.z], dtype=np.float64)


def _mliQuaternion(q):
    cdef mliQuaternion mliq
    mliq.w = q[0]
    mliq.x = q[1]
    mliq.y = q[2]
    mliq.z = q[3]
    return mliq


def _mliHomTraComp(tcomp):
    cdef mliHomTraComp mlitcomp
    mlitcomp.translation = _mliVec(tcomp[0:3])
    mlitcomp.rotation = _mliQuaternion(tcomp[3:7])
    return mlitcomp


def _mliHomTraComp2py(mliHomTraComp mlitcomp):
    tcomp = np.zeros(7, dtype=np.float64)
    tcomp[0:3] = _mliVec2py(mlitcomp.translation)
    tcomp[3:7] = _mliQuaternion2py(mlitcomp.rotation)
    return tcomp


def _mliMat2py(mliMat mlimat):
    mat = np.zeros(shape=(3, 3), dtype=np.float64)
    mat[0, 0] = mlimat.r00
    mat[0, 1] = mlimat.r01
    mat[0, 2] = mlimat.r02
    mat[1, 0] = mlimat.r10
    mat[1, 1] = mlimat.r11
    mat[1, 2] = mlimat.r12
    mat[2, 0] = mlimat.r20
    mat[2, 1] = mlimat.r21
    mat[2, 2] = mlimat.r22
    return mat


def _mliMat(mat):
    cdef mliMat mlimat
    mlimat.r00 = mat[0, 0]
    mlimat.r01 = mat[0, 1]
    mlimat.r02 = mat[0, 2]
    mlimat.r10 = mat[1, 0]
    mlimat.r11 = mat[1, 1]
    mlimat.r12 = mat[1, 2]
    mlimat.r20 = mat[2, 0]
    mlimat.r21 = mat[2, 1]
    mlimat.r22 = mat[2, 2]
    return mlimat


def quaternion_norm(quat):
    cdef mliQuaternion q
    q = _mliQuaternion(quat)
    return mliQuaternion_norm(q)


def quaternion_set_unit_xyz(double x, double y, double z):
    cdef mliQuaternion q
    q = mliQuaternion_set_unit_xyz(x, y, z)
    return _mliQuaternion2py(q)


def quaternion_set_tait_bryan(double rx, double ry, double rz):
    cdef mliQuaternion q
    q = mliQuaternion_set_tait_bryan(rx, ry, rz)
    return _mliQuaternion2py(q)


def quaternion_set_rotaxis_and_angle(
    rot_axis,
    double angle,
):
    cdef mliVec v
    v = _mliVec(rot_axis)
    cdef mliQuaternion q
    q = mliQuaternion_set_rotaxis_and_angle(v, angle)
    return _mliQuaternion2py(q)


def quaternion_to_matrix(quat):
    mliquat = _mliQuaternion(quat)
    mlimat = mliQuaternion_to_matrix(mliquat)
    return _mliMat2py(mlimat)


def HomTraComp_sequence(tcomp_a, tcomp_b):
    cdef mliHomTraComp mli_tcomp_a
    cdef mliHomTraComp mli_tcomp_b
    cdef mliHomTraComp mli_tcomp_c
    mli_tcomp_a = _mliHomTraComp(tcomp_a)
    mli_tcomp_b = _mliHomTraComp(tcomp_b)
    mli_tcomp_c = mliHomTraComp_sequence(mli_tcomp_a, mli_tcomp_b)
    return _mliHomTraComp2py(mli_tcomp_c)


MODE = {
    "pos": 0,
    "pos_inverse": 1,
    "dir": 2,
    "dir_inverse": 3,
}


def HomTraComp_apply(t_comp, vec_in, mode):
    cdef mliHomTraComp _t_comp = _mliHomTraComp(t_comp)

    assert mode in MODE, "mode is not known"
    assert vec_in is not None
    assert vec_in.shape[0] >= 1
    assert vec_in.shape[1] == 3

    cdef unsigned long num_vec = vec_in.shape[0]

    cdef cnp.ndarray[double, mode="c"] _vec_in = np.ascontiguousarray(
        vec_in.flatten(order="c"),
        dtype=np.float64,
    )

    cdef cnp.ndarray[double, mode="c"] _vec_out = np.zeros(
        (3* num_vec),
        dtype=np.float64,
    )

    cdef int rc

    rc = mliHomTraComp_transform(
        _t_comp,
        & _vec_in[0],
        & _vec_out[0],
        num_vec,
        mode=MODE[mode]
    )
    assert rc == 1, "mode is not known"

    return _vec_out.reshape((num_vec, 3))
