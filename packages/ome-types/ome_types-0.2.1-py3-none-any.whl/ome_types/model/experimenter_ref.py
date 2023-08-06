from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ExperimenterID


@ome_dataclass
class ExperimenterRef(Reference):
    """This empty element has a required Experimenter ID and an optional DocumentID
    attribute which refers to one of the Experimenters defined within OME.

    Parameters
    ----------
    id : ExperimenterID
    """

    id: ExperimenterID = EMPTY  # type: ignore
