from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .experimenter_ref import ExperimenterRef
from .leader import Leader
from .simple_types import ExperimenterGroupID


@ome_dataclass
class ExperimenterGroup:
    """The ExperimenterGroupID is required.

    Information should ideally be specified for at least one Leader as a contact
    for the group. The Leaders are themselves Experimenters.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    description : str, optional
        A description for the group.
    experimenter_ref : ExperimenterRef, optional
    id : ExperimenterGroupID
    leader : Leader, optional
    name : str, optional
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_ref: List[ExperimenterRef] = field(default_factory=list)
    id: ExperimenterGroupID = AUTO_SEQUENCE  # type: ignore
    leader: List[Leader] = field(default_factory=list)
    name: Optional[str] = None
