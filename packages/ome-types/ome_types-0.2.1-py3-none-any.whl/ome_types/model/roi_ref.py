from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ROIID


@ome_dataclass
class ROIRef(Reference):
    """ROIRef.

    Parameters
    ----------
    id : ROIID
    """

    id: ROIID = EMPTY  # type: ignore
