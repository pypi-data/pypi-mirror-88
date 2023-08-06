from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .experimenter_group_ref import ExperimenterGroupRef
from .experimenter_ref import ExperimenterRef
from .image_ref import ImageRef
from .simple_types import DatasetID


@ome_dataclass
class Dataset:
    """An element specifying a collection of images that are always processed
    together.

    Images can belong to more than one Dataset, and a Dataset may contain more
    than one Image. Images contain one or more DatasetRef elements to specify what
    datasets they belong to. Once a Dataset has been processed in any way, its
    collection of images cannot be altered. The ExperimenterRef and
    ExperimenterGroupRef elements specify the person and group this Dataset
    belongs to. Projects may contain one or more Datasets, and Datasets may belong
    to one or more Projects. This relationship is specified by listing DatasetRef
    elements within the Project element.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    description : str, optional
        A description for the dataset.
    experimenter_group_ref : ExperimenterGroupRef, optional
    experimenter_ref : ExperimenterRef, optional
    id : DatasetID
    image_ref : ImageRef, optional
    name : str, optional
        A name for the dataset that is suitable for presentation to the user.
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    experimenter_group_ref: Optional[ExperimenterGroupRef] = None
    experimenter_ref: Optional[ExperimenterRef] = None
    id: DatasetID = AUTO_SEQUENCE  # type: ignore
    image_ref: List[ImageRef] = field(default_factory=list)
    name: Optional[str] = None
