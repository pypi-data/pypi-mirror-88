from typing import Optional

from ome_types.dataclasses import EMPTY, ome_dataclass

from .settings import Settings
from .simple_types import LightSourceID, PercentFraction, PositiveFloat, UnitsLength


@ome_dataclass
class LightSourceSettings(Settings):
    """LightSourceSettings.

    Parameters
    ----------
    id : LightSourceID
    attenuation : PercentFraction, optional
        The Attenuation of the light source A fraction, as a value from 0.0 to
        1.0.
    wavelength : PositiveFloat, optional
        The Wavelength of the light source. Units are set by WavelengthUnit.
    wavelength_unit : UnitsLength, optional
        The units of the Wavelength of the light source - default:nanometres
    """

    id: LightSourceID = EMPTY  # type: ignore
    attenuation: Optional[PercentFraction] = None
    wavelength: Optional[PositiveFloat] = None
    wavelength_unit: Optional[UnitsLength] = UnitsLength("nm")
