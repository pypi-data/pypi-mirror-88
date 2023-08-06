from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import MicrobeamManipulationID


@ome_dataclass
class MicrobeamManipulationRef(Reference):
    """MicrobeamManipulationRef.

    Parameters
    ----------
    id : MicrobeamManipulationID
    """

    id: MicrobeamManipulationID = EMPTY  # type: ignore
