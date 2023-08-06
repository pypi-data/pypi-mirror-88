from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import AnnotationID


@ome_dataclass
class AnnotationRef(Reference):
    """The AnnotationRef element is a reference to an element derived from the
    CommonAnnotation element.

    Parameters
    ----------
    id : AnnotationID
    """

    id: AnnotationID = EMPTY  # type: ignore
