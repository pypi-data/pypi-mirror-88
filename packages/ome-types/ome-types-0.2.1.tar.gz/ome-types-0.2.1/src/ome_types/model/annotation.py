from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .simple_types import AnnotationID, ExperimenterID


@ome_dataclass
class Annotation:
    """An annotation from which all others are ultimately derived.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    annotator : ExperimenterID, optional
        The Annotator is the person who attached this annotation. e.g. If
        UserA annotates something with TagB, owned by UserB, UserA is still
        the Annotator.
    description : str, optional
        A description for the annotation.
    id : AnnotationID
    namespace : str, optional
        We recommend the inclusion of a namespace for annotations you define.
        If it is absent then we assume the annotation is to use our (OME's)
        default interpretation for this type.
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    annotator: Optional[ExperimenterID] = None
    description: Optional[str] = None
    id: AnnotationID = AUTO_SEQUENCE  # type: ignore
    namespace: Optional[str] = None
