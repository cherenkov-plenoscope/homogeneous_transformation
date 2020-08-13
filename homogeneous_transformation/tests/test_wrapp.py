import homogeneous_transformation as ht
import numpy as np

def test_quaternion_unity():

    a = ht.quaternion.set_rotaxis_and_angle(rot_axis=[0, 0, 1], angle=0.0)
    b = ht.quaternion.set_tait_bryan(x_angle=0, y_angle=0, z_angle=0)
    c = ht.quaternion.set_unit_xyz(x=0, y=0, z=0)
    d = ht.Quaternion(w=1, x=0, y=0, z=0)

    assert a == b
    assert a == c
    assert a == d


def test_quaternion_forth_and_back():
    t_AB = ht.HomTra(
        translation=ht.Vec(x=0.0, y=0.0, z=1.0),
        rotation=ht.quaternion.set_tait_bryan(0.0, 0.0, np.deg2rad(45)),
    )

    pos_A = [0.0, 0.0, 1.0]

    pos_B = ht.transform.position(t_AB, pos_A)
    pos_A_back = ht.transform.position_inverse(t_AB, pos_B)

    assert pos_A_back[0] == pos_A[0]
    assert pos_A_back[1] == pos_A[1]
    assert pos_A_back[2] == pos_A[2]


def test_sequence():
    t_AB = ht.HomTra(
        translation=ht.Vec(0, 0, 0),
        rotation=ht.quaternion.set_tait_bryan(np.deg2rad(45), 0, 0),
    )
    t_BC = ht.HomTra(
        translation=ht.Vec(0, 0, 0),
        rotation=ht.quaternion.set_tait_bryan(
            np.deg2rad(45),
            np.deg2rad(45),
            0
        ),
    )
    t_AC = ht.sequence(t_AB, t_BC)

    pos_A = [1.0, 2.0, 3.0]
    pos_B = ht.transform.position(t_AB, pos_A)

    pos_C = ht.transform.position(t_BC, pos_B)
    pos_C_direct = ht.transform.position(t_AC, pos_A)

    assert np.abs(pos_C[0] - pos_C_direct[0]) < 1e-6
    assert np.abs(pos_C[1] - pos_C_direct[1]) < 1e-6
    assert np.abs(pos_C[2] - pos_C_direct[2]) < 1e-6
