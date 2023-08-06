from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .annotation_ref import AnnotationRef
from .numeric_annotation import NumericAnnotation


@ome_dataclass
class DoubleAnnotation(NumericAnnotation):
    """A simple numerical annotation of type xsd:double

    Parameters
    ----------
    value : float
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

    value: float = EMPTY  # type: ignore
    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
