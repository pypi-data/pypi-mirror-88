from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ExperimenterGroupID


@ome_dataclass
class ExperimenterGroupRef(Reference):
    """This empty element has a reference (the ExperimenterGroup ID attribute) to a
    ExperimenterGroup defined within OME.

    Parameters
    ----------
    id : ExperimenterGroupID
    """

    id: ExperimenterGroupID = EMPTY  # type: ignore
