import homogeneous_transformation as ht
import numpy as np


A = {
    "pos": [1.0, 0.0, 0.0],
    "rot": {
        "repr": "axis_angle",
        "axis": [0.0, 0.0, 1.0],
        "angle_deg": 0.3,
    },
}

B = {
    "pos": [0.0, 30.0, 1.0],
    "rot": {
        "repr": "tait_bryan",
        "xyz_deg": [1.0, 2.0, 45.0],
    },
}

C = {
    "pos": [0.0, 1.0, 1.0],
    "rot": {
        "repr": "quaternion",
        "xyz": [0.0, 0.1, 0.2],
    },
}


def assert_ray_almost_equal(a, b, margin):
    np.testing.assert_array_almost_equal(a[0], b[0], margin)
    np.testing.assert_array_almost_equal(a[1], b[1], margin)


def test_zeros():
    t = ht.zeros()
    assert isinstance(t, np.ndarray)
    assert t.dtype == np.float64
    assert t.shape == (7,)
    assert np.all(t == 0.0)


def test_unity():
    t = ht.unity()
    assert isinstance(t, np.ndarray)
    assert t.dtype == np.float64
    assert t.shape == (7,)
    assert np.all(ht.get_translation_vector(t) == 0.0)
    rot_matrix = ht.quaternion.to_matrix(quat=ht.get_rotation_quaternion(t))
    np.testing.assert_array_almost_equal(rot_matrix, np.eye(3), 1e-9)


def test_set_get_translation():
    vec = np.array([1, 2, 3])
    t = ht.unity()
    t = ht.set_translation_vector(t, vec)
    vecb = ht.get_translation_vector(t)
    np.testing.assert_array_almost_equal(vecb, vec)


def test_set_get_rotation():
    quat = ht.quaternion.set_tait_bryan(rx=0.1, ry=-0.4, rz=0.2)
    t = ht.unity()
    t = ht.set_rotation_quaternion(t, quat)
    assert np.all(ht.get_translation_vector(t) == 0.0)
    quatb = ht.get_rotation_quaternion(t)
    np.testing.assert_array_almost_equal(quatb, quat)


def test_ray():
    prng = np.random.Generator(np.random.PCG64(1337))

    for T in [A, B, C]:
        t = ht.compile(T)
        for i in range(50):
            for j in range(50):
                support = np.array(
                    [
                        prng.uniform(),
                        prng.uniform(),
                        prng.uniform(),
                    ]
                )

                direction = np.array(
                    [
                        prng.uniform(),
                        prng.uniform(),
                        prng.uniform(),
                    ]
                )

                direction = direction / np.linalg.norm(direction)

                ray = (support, direction)

                t_ray = ht.transform_ray(t, ray[0], ray[1])
                ray_back = ht.transform_ray_inverse(t, t_ray[0], t_ray[1])

                assert_ray_almost_equal(ray, ray_back, 1e-9)


def test_shapes_two_dim():
    prng = np.random.Generator(np.random.PCG64(42))
    tA = ht.compile(A)

    p = prng.uniform(size=(100, 3))
    assert p.shape == (100, 3)

    tp = ht.transform_position(t=tA, p=p)
    assert tp.shape == (100, 3)


def test_shapes_one_dim():
    prng = np.random.Generator(np.random.PCG64(42))
    tA = ht.compile(A)

    p = prng.uniform(size=(3,))
    assert p.shape == (3,)

    tp = ht.transform_position(t=tA, p=p)
    assert tp.shape == (3,)


def test_to_matrix():
    for T in [A, B, C]:
        t = ht.compile(T)
        v = ht.get_translation_vector(t)
        m = ht.to_matrix(t=t)

        # lower row
        # ----------
        assert m.shape == (4, 4)
        assert m[3, 0] == 0
        assert m[3, 1] == 0
        assert m[3, 2] == 0
        assert m[3, 3] == 1

        # test translation vector
        # -----------------------
        assert m[0, 3] == v[0]
        assert m[1, 3] == v[1]
        assert m[2, 3] == v[2]

        # rotmatrix is normalized
        # -----------------------
        assert np.abs(np.linalg.norm(m[0:3, 0]) - 1.0) < 1e-9
        assert np.abs(np.linalg.norm(m[0:3, 1]) - 1.0) < 1e-9
        assert np.abs(np.linalg.norm(m[0:3, 2]) - 1.0) < 1e-9


def sequence():
    for T1 in [A, B, C]:
        t1 = ht.compile(T1)
        for T2 in [A, B, C]:
            t2 = ht.compile(T2)
            t12 = ht.sequence(t1, t2)
