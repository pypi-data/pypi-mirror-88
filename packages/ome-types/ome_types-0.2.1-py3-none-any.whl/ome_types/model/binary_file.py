from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .bin_data import BinData
from .external import External
from .simple_types import NonNegativeLong


@ome_dataclass
class BinaryFile:
    """Describes a binary file.

    Parameters
    ----------
    file_name : str
    size : NonNegativeLong
        Size of the uncompressed file.
    bin_data : BinData, optional
    external : External, optional
    mime_type : str, optional
    """

    file_name: str
    size: NonNegativeLong
    bin_data: Optional[BinData] = None
    external: Optional[External] = None
    mime_type: Optional[str] = None
