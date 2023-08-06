from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import LightSourceID, UnitsPower


@ome_dataclass
class LightSource(ManufacturerSpec):
    """The lightsource for the instrument.

    An instrument may have several light sources. The type of lightsource is
    specified by one of the child-elements which are 'Laser', 'Filament', 'Arc' or
    'LightEmittingDiode'. Each of the light source types has its own Type
    attribute to further differentiate the light source (eg, Nd-YAG for Laser or
    Hg for Arc).

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    id : LightSourceID
        A LightSource ID must be specified for each light source, and the
        individual light sources can be referred to by their LightSource IDs
        (eg from Channel).
    lot_number : str, optional
        The lot number of the component.
    manufacturer : str, optional
        The manufacturer of the component.
    model : str, optional
        The Model of the component.
    power : float, optional
        The light-source power. Units are set by PowerUnit.
    power_unit : UnitsPower, optional
        The units of the Power - default:milliwatts.
    serial_number : str, optional
        The serial number of the component.
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    id: LightSourceID = AUTO_SEQUENCE  # type: ignore
    power: Optional[float] = None
    power_unit: Optional[UnitsPower] = UnitsPower("mW")
