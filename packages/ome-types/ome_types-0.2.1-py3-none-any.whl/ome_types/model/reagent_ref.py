from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ReagentID


@ome_dataclass
class ReagentRef(Reference):
    """ReagentRef.

    Parameters
    ----------
    id : ReagentID
    """

    id: ReagentID = EMPTY  # type: ignore
