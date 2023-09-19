"""
Define, sequence, and apply transformations in 3D.
"""
from .version import __version__
from . import merlict_c89
from . import quaternion
import numpy as np


EXAMPLE_CIVIL = {
    "pos": np.array([1.0, 0.0, 0.0]),
    "rot": {
        "repr": "axis_angle",
        "axis": np.array([0.0, 0.0, 1.0]),
        "angle_deg": 0.3,
    },
}


def zeros():
    """
    Returns a transformation all set to zero. (not a valid rotation)
    """
    return np.zeros(7, dtype=np.float64)


def unity():
    """
    Returns the unit-transformation.
    """
    t = zeros()
    t = set_rotation_quaternion(
        t, quaternion.set_tait_bryan(rx=0.0, ry=0.0, rz=0.0)
    )
    return t


def get_translation_vector(t):
    return t[0:3]


def set_translation_vector(t, vec):
    t[0:3] = vec
    return t


def get_rotation_quaternion(t):
    return t[3:7]


def set_rotation_quaternion(t, quat):
    t[3:7] = quat
    return t


def compile(t_civil, quaternion_norm_margin=1e-6):
    """
    Returns a transformation in compact representation.

    Parameters
    ----------
    t_civil : dict
        A transformation in civil representation.
    """
    vec = np.array(t_civil["pos"])
    quat = quaternion.compile(
        rot_civil=t_civil["rot"],
        quaternion_norm_margin=quaternion_norm_margin,
    )

    t = zeros()
    t = set_translation_vector(t=t, vec=vec)
    t = set_rotation_quaternion(t=t, quat=quat)
    return t


def sequence(t_a, t_b):
    """
    Computes the homogenous transformation from the concatenation of
    't_a' and 't_b'.

    Parameters
    ----------
    t_a : array[7], float
        Transformation 'a' in compact representation.
    t_b : array[7], float
        Transformation 'b' in compact representation.

    Returns
    -------
    t_ba : array[7], float
        Transformation 'b*a' in compact representation.
    """
    return merlict_c89.wrapper.HomTraComp_sequence(t_a, t_b)


def transform_position(t, p):
    return _transform(t=t, v=p, mode="pos")


def transform_position_inverse(t, p):
    return _transform(t=t, v=p, mode="pos_inverse")


def transform_orientation(t, d):
    return _transform(t=t, v=d, mode="dir")


def transform_orientation_inverse(t, d):
    return _transform(t=t, v=d, mode="dir_inverse")


def transform_ray(t, ray_supports, ray_directions):
    oray_supports = transform_position(t=t, p=ray_supports)
    oray_directions = transform_orientation(t=t, d=ray_directions)
    return oray_supports, oray_directions


def transform_ray_inverse(t, ray_supports, ray_directions):
    oray_supports = transform_position_inverse(t=t, p=ray_supports)
    oray_directions = transform_orientation_inverse(t=t, d=ray_directions)
    return oray_supports, oray_directions


def to_matrix(t):
    """
    Returns the (4, 4) homogenous transformation matrix represented by 't'.
    """
    vec = get_translation_vector(t)
    quat = get_rotation_quaternion(t)
    rot_matrix = quaternion.to_matrix(quat)
    m = np.zeros(shape=(4, 4), dtype=np.float64)
    m[0:3, 0:3] = rot_matrix
    m[0:3, 3] = vec
    m[3, 3] = 1.0
    return m


def _shape_forth(v):
    if not isinstance(v, np.ndarray):
        v = np.array(v)
    dim = len(v.shape)
    if dim == 1:
        assert v.shape[0] == 3, "Expected one 3D vector."
        v = v.reshape((1, 3))
    elif dim == 2:
        assert v.shape[1] == 3
    else:
        raise AssertionError("Expected 1 or 2 dims.")
    return dim, v


def _shape_back(r, dim):
    if dim == 1:
        return r.reshape((3,))
    elif dim == 2:
        return r
    else:
        raise AssertionError("Expected 1 or 2 dims.")


def _transform(t, v, mode):
    """
    A wrapper to handle the shape of the input and output.
    If the input had only 1 dimension, i.e. shape == (3,) then
    we also want the output to have this dimension.
    """
    dim, p = _shape_forth(v=v)
    r = merlict_c89.wrapper.HomTraComp_apply(t, p, mode=mode)
    return _shape_back(r=r, dim=dim)
