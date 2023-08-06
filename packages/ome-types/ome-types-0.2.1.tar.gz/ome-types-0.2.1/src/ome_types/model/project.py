from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .dataset_ref import DatasetRef
from .experimenter_group_ref import ExperimenterGroupRef
from .experimenter_ref import ExperimenterRef
from .simple_types import ProjectID


@ome_dataclass
class Project:
    """The Project ID is required.

    Datasets can be grouped into projects using a many-to-many relationship. A
    Dataset may belong to one or more Projects by including one or more ProjectRef
    elements which refer to Project IDs. Projects do not directly contain images -
    only by virtue of containing datasets, which themselves contain images.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    dataset_ref : DatasetRef, optional
    description : str, optional
        A description for the project.
    experimenter_group_ref : ExperimenterGroupRef, optional
    experimenter_ref : ExperimenterRef, optional
    id : ProjectID
    name : str, optional
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    dataset_ref: List[DatasetRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_group_ref: Optional[ExperimenterGroupRef] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    id: ProjectID = AUTO_SEQUENCE  # type: ignore
    name: Optional[str] = None
