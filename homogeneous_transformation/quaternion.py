from . import merlict_c89
import numpy as np


def _assert_unit_quaternion(q, quaternion_norm_margin):
    q_margin = np.abs(merlict_c89.wrapper.quaternion_norm(q) - 1.0)
    assert q_margin < quaternion_norm_margin, "Expected a unit-quaternion."


def compile(rot_civil, quaternion_norm_margin=1e-6):
    """
    Returns a unit-quaternion representing the desired rotation.

    Parameters
    ----------
    rot_civil : dict
        This is the 'rot' part in the civil representation.
        A 'rot' has its own representation 'repr' which must be either of:
        'tait_bryan', 'axis_angle', or 'quaternion'.
    """
    rt = rot_civil
    assert (
        "repr" in rt
    ), "Expected 'rot_civil' to define its own representation 'repr'."

    if rt["repr"] == "tait_bryan":
        return set_tait_bryan(
            rx=np.deg2rad(rt["xyz_deg"][0]),
            ry=np.deg2rad(rt["xyz_deg"][1]),
            rz=np.deg2rad(rt["xyz_deg"][2]),
        )
    elif rt["repr"] == "axis_angle":
        rot_axis = np.array(rt["axis"])
        angle = np.deg2rad(rt["angle_deg"])
        return set_axis_angle(
            rot_axis=rot_axis,
            angle=angle,
        )
    elif rt["repr"] == "quaternion":
        q = set_unit_xyz(
            x=rt["xyz"][0],
            y=rt["xyz"][1],
            z=rt["xyz"][2],
        )
        _assert_unit_quaternion(
            q=q, quaternion_norm_margin=quaternion_norm_margin
        )
        return q
    else:
        raise AssertionError("Unknown representation 'repr' in 'rot_civil'.")


def set_unit_xyz(x, y, z):
    return merlict_c89.wrapper.quaternion_set_unit_xyz(x, y, z)


def set_axis_angle(rot_axis, angle):
    """
    Parameters
    ----------
    rot_axis : array[3], float
        Rotation axis.
    angle : float
        Rotation angle/rad.
    """
    return merlict_c89.wrapper.quaternion_set_rotaxis_and_angle(
        rot_axis,
        angle,
    )


def set_tait_bryan(rx, ry, rz):
    """
    Define a rotation using tait-bryan-angles.

    Parameters
    ----------
    rx : float
        Rotation angle in x/rad.
    ry : float
        Rotation angle in y/rad.
    rz : float
        Rotation angle in z/rad.
    """
    return merlict_c89.wrapper.quaternion_set_tait_bryan(rx, ry, rz)


def to_matrix(quat):
    """
    Returns the rotation-matrix represented by quat.
    """
    return merlict_c89.wrapper.quaternion_to_matrix(quat)
