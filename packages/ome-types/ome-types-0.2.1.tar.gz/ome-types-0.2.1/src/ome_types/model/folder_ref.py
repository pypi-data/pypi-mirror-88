from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import FolderID


@ome_dataclass
class FolderRef(Reference):
    """The FolderRef element refers to a Folder by specifying the Folder ID
    attribute.

    One or more FolderRef elements may be listed within the Folder element to
    specify what Folders the Folder contains. This tree hierarchy must be acyclic.

    Parameters
    ----------
    id : FolderID
    """

    id: FolderID = EMPTY  # type: ignore
