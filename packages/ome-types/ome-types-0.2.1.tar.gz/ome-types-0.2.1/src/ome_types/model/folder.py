from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .folder_ref import FolderRef
from .image_ref import ImageRef
from .roi_ref import ROIRef
from .simple_types import FolderID


@ome_dataclass
class Folder:
    """An element specifying a possibly heterogeneous collection of data.

    Folders may contain Folders so that data may be organized within a tree of
    Folders. Data may be in multiple Folders but a Folder may not be in more than
    one other Folder.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    description : str, optional
        A description for the folder.
    folder_ref : FolderRef, optional
    id : FolderID
    image_ref : ImageRef, optional
    name : str, optional
        A name for the folder that is suitable for presentation to the user.
    roi_ref : ROIRef, optional
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    folder_ref: List[FolderRef] = field(default_factory=list)
    id: FolderID = AUTO_SEQUENCE  # type: ignore
    image_ref: List[ImageRef] = field(default_factory=list)
    name: Optional[str] = None
    roi_ref: List[ROIRef] = field(default_factory=list)
