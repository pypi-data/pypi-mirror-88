from ome_types.dataclasses import ome_dataclass

from .annotation import Annotation


@ome_dataclass
class TextAnnotation(Annotation):
    """An abstract Text Annotation from which some others are derived.

    Parameters
    ----------
    annotator : ExperimenterID, optional
        The Annotator is the person who attached this annotation. e.g. If
        UserA annotates something with TagB, owned by UserB, UserA is still
        the Annotator.
    id : AnnotationID
    namespace : str, optional
        We recommend the inclusion of a namespace for annotations you define.
        If it is absent then we assume the annotation is to use our (OME's)
        default interpretation for this type.
    """
