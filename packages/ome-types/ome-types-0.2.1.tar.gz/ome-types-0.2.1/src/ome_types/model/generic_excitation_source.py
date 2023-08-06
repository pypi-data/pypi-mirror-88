from typing import Optional

from ome_types.dataclasses import ome_dataclass

from .light_source import LightSource
from .map import Map


@ome_dataclass
class GenericExcitationSource(LightSource):
    """The GenericExcitationSource element is used to represent a source as a
    collection of key/value pairs, stored in a Map.

    The other lightsource objects should always be used in preference to this if
    possible.

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
    map : Map, optional
    model : str, optional
        The Model of the component.
    power : float, optional
        The light-source power. Units are set by PowerUnit.
    power_unit : UnitsPower, optional
        The units of the Power - default:milliwatts.
    serial_number : str, optional
        The serial number of the component.
    """

    map: Optional[Map] = None
