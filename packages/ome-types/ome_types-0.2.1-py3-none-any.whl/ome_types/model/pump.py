from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import LightSourceID


@ome_dataclass
class Pump(Reference):
    """The Pump element is a reference to a LightSource.

    It is used within the Laser element to specify the light source for the
    laser's pump (if any).

    Parameters
    ----------
    id : LightSourceID
    """

    id: LightSourceID = EMPTY  # type: ignore
