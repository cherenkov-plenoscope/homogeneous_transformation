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
    pass


cdef extern from "merlict_c89/merlict_c89/mliRotMat.h":
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


@cython.embedsignature(True)
def Quaternion_set_tait_bryan(x_angle, y_angle, z_angle):
    q = mliQuaternion_set_tait_bryan(x_angle, y_angle, z_angle)
    return Quaternion(q.w, q.x, q.y, q.z)


@cython.embedsignature(True)
def Quaternion_set_rotaxis_and_angle(rot_axis, angle):
    q = mliQuaternion_set_rotaxis_and_angle(
        mliVec_set(rot_axis[0], rot_axis[1], rot_axis[2]),
        angle
    )
    return Quaternion(q.w, q.x, q.y, q.z)


@cython.embedsignature(True)
def Quaternion_set_unit_xyz(x, y, z):
    q = mliQuaternion_set_unit_xyz(x, y, z)
    return Quaternion(q.w, q.x, q.y, q.z)


@cython.embedsignature(True)
def sequence(homtra_A_to_B, homtra_B_to_C):
    """
    Return the homogenous transformation (a_to_d) by estimating the sequence
    along (a_to_b) and (b_to_d).
    """
    ab = homtra_A_to_B
    bc = homtra_B_to_C
    _ab = mliHomTraComp_set(
        mliVec_set(ab.trans.x, ab.trans.y, ab.trans.z),
        mliQuaternion_set(ab.rot.w, ab.rot.x, ab.rot.y, ab.rot.z)
    )
    _bc = mliHomTraComp_set(
        mliVec_set(bc.trans.x, bc.trans.y, bc.trans.z),
        mliQuaternion_set(bc.rot.w, bc.rot.x, bc.rot.y, bc.rot.z)
    )
    _ac = mliHomTraComp_sequence(_ab, _bc)
    return HomTra(
        rot=Quaternion(_ac.rot.w, _ac.rot.x, _ac.rot.y, _ac.rot.z),
        trans=Vec(_ac.trans.x, _ac.trans.y, _ac.trans.z)
    )


cdef mliHomTra _extract_homtra(homtra):
    _homtra_comp = mliHomTraComp_set(
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
    return mliHomTra_from_compact(_homtra_comp)


@cython.embedsignature(True)
def transform_position(homtra_A_to_B, position_wrt_A):
    """
    returns position w.r.t. B.
    """
    pA = position_wrt_A
    _homtra_AB = _extract_homtra(homtra_A_to_B)
    _pB = mliHomTra_pos(
        &_homtra_AB,
        mliVec_set(pA[0], pA[1], pA[2])
    )
    return [_pB.x, _pB.y, _pB.z]


@cython.embedsignature(True)
def transform_position_inverse(homtra_A_to_B, position_wrt_B):
    """
    returns position w.r.t. A.
    """
    pB = position_wrt_B
    _homtra_AB = _extract_homtra(homtra_A_to_B)
    _pA = mliHomTra_pos_inverse(
        &_homtra_AB,
        mliVec_set(pB[0], pB[1], pB[2])
    )
    return [_pA.x, _pA.y, _pA.z]


@cython.embedsignature(True)
def transform_direction(homtra_A_to_B, direction_wrt_A):
    """
    returns direction w.r.t. A.
    """
    dA = direction_wrt_A
    _homtra_AB = _extract_homtra(homtra_A_to_B)
    _dB = mliHomTra_dir(
        &_homtra_AB,
        mliVec_set(dA[0], dA[1], dA[2])
    )
    return [_dB.x, _dB.y, _dB.z]


@cython.embedsignature(True)
def transform_direction_inverse(homtra_A_to_B, direction_wrt_B):
    """
    returns direction w.r.t. B.
    """
    dB = direction_wrt_B
    _homtra_AB = _extract_homtra(homtra_A_to_B)
    _dA = mliHomTra_dir_inverse(
        &_homtra_AB,
        mliVec_set(dB[0], dB[1], dB[2])
    )
    return [_dA.x, _dA.y, _dA.z]
