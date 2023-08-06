from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ExperimenterID


@ome_dataclass
class Leader(Reference):
    """Contact information for a ExperimenterGroup leader specified using a reference
    to an Experimenter element defined elsewhere in the document.

    Parameters
    ----------
    id : ExperimenterID
    """

    id: ExperimenterID = EMPTY  # type: ignore
