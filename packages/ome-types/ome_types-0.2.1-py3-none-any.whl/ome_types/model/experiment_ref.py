from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import ExperimentID


@ome_dataclass
class ExperimentRef(Reference):
    """ExperimentRef.

    Parameters
    ----------
    id : ExperimentID
    """

    id: ExperimentID = EMPTY  # type: ignore
