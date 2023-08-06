from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ProjectID


@ome_dataclass
class ProjectRef(Reference):
    """There may be one or more of these in a Dataset.

    This empty element has a required Project ID attribute that refers to Projects
    defined within the OME element.

    Parameters
    ----------
    id : ProjectID
    """

    id: ProjectID = EMPTY  # type: ignore
