#########################
Homogenous Transformation
#########################
|TestStatus| |PyPiStatus| |BlackStyle|

Define, sequence, and apply transformations in 3D.
Taken from `merlict_c89_link`_ and wrapped in python with a numpy friendly interface.

******
Define
******

.. code-block:: python

    t_civil = {
        "pos": [1.0, 0.0, 0.0],
        "rot": {
            "repr": "axis_angle",
            "axis":[0.0, 0.0, 1.0],
            "angle_deg": 0.3,
        },
    }


Transformations can be defined with a civil representation in a dict.
The rotation can be represented by either 'axis_angle', 'tait_bryan', or
'quaternion'. To apply the transformation we compile it.

.. code-block:: python

    import homogeneous_transformation as ht
    t = ht.compile(t_civil)


The civil representation can be compiled into a compact numpy array ``t``
of shape ``(7, )``.

.. code-block:: python

    In : t
    Out: array([1. , 0. , 0. , 0.99999657, 0. , 0. , 0.00261799])


The first 3 fields are the translation vector and the remaining 4 fields are
the rotation quaternion.
One can also export this with  ``to_matrix`` into a homogenous
transformation matrix of shape ``(4, 4)``.

.. code-block::

    In : ht.to_matrix(t)
    Out:
    array([[ 0.99998629, -0.00523596,  0.        ,  1.        ],
           [ 0.00523596,  0.99998629,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  1.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  1.        ]])

********
Sequence
********

Transformations in compact representation can be concatenated to compute the
sequence.

.. code-block:: python

    t_ab = ht.sequence(t_a, t_b)


*****
Apply
*****

Apply transformations to positions, orientations, or rays.

.. code-block:: python

    import numpy as np

    vec = np.array([0, 0, 1])

    t_vec = ht.transform_position(t, vec)


Here ``vec`` can either be a single vector of shape ``(3, )`` or an
array of ``N`` vectors with shape ``(N, 3)``.
The loop over the individual vectors is in the ``C`` backend and
thus very efficient.


.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/homogeneous_transformation/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/homogeneous_transformation/actions/workflows/test.yml

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/homogeneous_transformation
    :target: https://pypi.org/project/homogeneous_transformation

.. _merlict_c89_link: https://github.com/cherenkov-plenoscope/merlict_c89