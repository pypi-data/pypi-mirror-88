from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import DichroicID


@ome_dataclass
class DichroicRef(Reference):
    """DichroicRef.

    Parameters
    ----------
    id : DichroicID
    """

    id: DichroicID = EMPTY  # type: ignore
