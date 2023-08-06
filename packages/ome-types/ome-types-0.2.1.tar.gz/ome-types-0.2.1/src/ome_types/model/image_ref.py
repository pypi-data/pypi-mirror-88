from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ImageID


@ome_dataclass
class ImageRef(Reference):
    """The ImageRef element is a reference to an Image element.

    Parameters
    ----------
    id : ImageID
    """

    id: ImageID = EMPTY  # type: ignore
