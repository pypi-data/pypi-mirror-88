from ome_types.dataclasses import ome_dataclass


@ome_dataclass
class AffineTransform:
    """A matrix used to transform the shape.

    ⎡ A00, A01, A02 ⎤ ⎢ A10, A11, A12 ⎥ ⎣ 0,   0,   1   ⎦

    Parameters
    ----------
    a00 : float
    a01 : float
    a02 : float
    a10 : float
    a11 : float
    a12 : float
    """

    a00: float
    a01: float
    a02: float
    a10: float
    a11: float
    a12: float
