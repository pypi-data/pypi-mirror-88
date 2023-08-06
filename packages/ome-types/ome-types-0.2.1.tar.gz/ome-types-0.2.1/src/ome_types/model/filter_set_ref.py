from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import FilterSetID


@ome_dataclass
class FilterSetRef(Reference):
    """FilterSetRef.

    Parameters
    ----------
    id : FilterSetID
    """

    id: FilterSetID = EMPTY  # type: ignore
