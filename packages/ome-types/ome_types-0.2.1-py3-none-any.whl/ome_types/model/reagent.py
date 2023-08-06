from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .simple_types import ReagentID


@ome_dataclass
class Reagent:
    """Reagent is used to describe a chemical or some other physical experimental
    parameter.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    description : str, optional
        A long description for the reagent.
    id : ReagentID
    name : str, optional
        A short name for the reagent
    reagent_identifier : str, optional
        This is a reference to an external (to OME) representation of the
        Reagent. It serves as a foreign key into an external database. - It is
        sometimes referred to as ExternalIdentifier.
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    id: ReagentID = AUTO_SEQUENCE  # type: ignore
    name: Optional[str] = None
    reagent_identifier: Optional[str] = None
