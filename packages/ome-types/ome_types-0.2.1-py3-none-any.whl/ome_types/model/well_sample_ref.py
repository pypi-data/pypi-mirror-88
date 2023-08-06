from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import WellSampleID


@ome_dataclass
class WellSampleRef(Reference):
    """The WellSampleRef element is a reference to a WellSample element.

    Parameters
    ----------
    id : WellSampleID
    """

    id: WellSampleID = EMPTY  # type: ignore
