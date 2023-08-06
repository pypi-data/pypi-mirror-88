from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import FilterID


@ome_dataclass
class FilterRef(Reference):
    """FilterRef.

    Parameters
    ----------
    id : FilterID
    """

    id: FilterID = EMPTY  # type: ignore
