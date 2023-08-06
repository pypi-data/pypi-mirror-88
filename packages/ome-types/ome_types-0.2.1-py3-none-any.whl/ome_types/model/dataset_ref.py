from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import DatasetID


@ome_dataclass
class DatasetRef(Reference):
    """The DatasetRef element refers to a Dataset by specifying the Dataset ID
    attribute.

    One or more DatasetRef elements may be listed within the Image element to
    specify what Datasets the Image belongs to.

    Parameters
    ----------
    id : DatasetID
    """

    id: DatasetID = EMPTY  # type: ignore
