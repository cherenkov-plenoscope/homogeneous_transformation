# Homogeneous Transformation
Transform position vectors or direction vectors in between 3D frames.
Taken from [```merlict_c89```](https://github.com/cherenkov-plenoscope/merlict_c89) and wrapped in python.

## define rotations
```python
import homogeneous_transformation as ht

q = ht.quaternion.set_rotaxis_and_angle(rot_axis, angle)
q = ht.quaternion.set_tait_bryan(x_angle, y_angle, z_angle)
q = ht.quaternion.set_unit_xyz(x, y, z)
q = ht.Quaternion(w, x, y, z)
```

## position
```python
import numpy as np
import homogeneous_transformation as ht

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
```


## direction
```python
d_B = ht.transform.direction(t_AB, [0.0, 1.0, 0.0])
```
```bash
Out[5]: [0.7071, 0.7071, 0.0]
```

## sequence
```python
t_BC = ht.HomTra(
    translation=ht.Vec(x=0.0, y=-2.0, z=0.0),
    rotation=ht.quaternion.set_tait_bryan(0, np.deg2rad(15), 0),
)

t_AC = ht.sequence(t_AB, t_BC)
```

#### Download
```bash
git clone --recursive git@github.com:cherenkov-plenoscope/homogeneous_transformation.git
```

#### Install
```bash
pip install -e homogeneous_transformation/
```

#### Update
```bash
git pull
git submodule update
```
