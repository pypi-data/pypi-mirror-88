from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ChannelID


@ome_dataclass
class ChannelRef(Reference):
    """ChannelRef.

    Parameters
    ----------
    id : ChannelID
    """

    id: ChannelID = EMPTY  # type: ignore
