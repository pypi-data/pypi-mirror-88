from dataclasses import field
from enum import Enum
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .experimenter_ref import ExperimenterRef
from .light_source_settings import LightSourceSettings
from .roi_ref import ROIRef
from .simple_types import MicrobeamManipulationID


class Type(Enum):
    """The type of manipulation performed."""

    FLIP = "FLIP"
    FRAP = "FRAP"
    INVERSE_FRAP = "InverseFRAP"
    OPTICAL_TRAPPING = "OpticalTrapping"
    OTHER = "Other"
    PHOTOABLATION = "Photoablation"
    PHOTOACTIVATION = "Photoactivation"
    UNCAGING = "Uncaging"


@ome_dataclass
class MicrobeamManipulation:
    """Defines a microbeam operation type and the region of the image it was applied
    to.

    The LightSourceRef element is a reference to a LightSource specified in the
    Instrument element which was used for a technique other than illumination for
    the purpose of imaging. For example, a laser used for photobleaching.

    Parameters
    ----------
    experimenter_ref : ExperimenterRef
    roi_ref : ROIRef
    description : str, optional
        A description for the Microbeam Manipulation.
    id : MicrobeamManipulationID
    light_source_settings : LightSourceSettings, optional
    type : Type, optional
        The type of manipulation performed.
    """

    experimenter_ref: ExperimenterRef
    roi_ref: List[ROIRef]
    description: Optional[str] = None
    id: MicrobeamManipulationID = AUTO_SEQUENCE  # type: ignore
    light_source_settings: List[LightSourceSettings] = field(default_factory=list)
    type: List[Type] = field(default_factory=list)
