from dataclasses import field
from typing import List, Optional

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .dichroic_ref import DichroicRef
from .filter_ref import FilterRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import FilterSetID


@ome_dataclass
class FilterSet(ManufacturerSpec):
    """Filter set manufacturer specification

    Parameters
    ----------
    dichroic_ref : DichroicRef, optional
    emission_filter_ref : FilterRef, optional
        The Filters placed in the Emission light path.
    excitation_filter_ref : FilterRef, optional
        The Filters placed in the Excitation light path.
    id : FilterSetID
    lot_number : str, optional
        The lot number of the component.
    manufacturer : str, optional
        The manufacturer of the component.
    model : str, optional
        The Model of the component.
    serial_number : str, optional
        The serial number of the component.
    """

    dichroic_ref: Optional[DichroicRef] = None
    emission_filter_ref: List[FilterRef] = field(default_factory=list)
    excitation_filter_ref: List[FilterRef] = field(default_factory=list)
    id: FilterSetID = AUTO_SEQUENCE  # type: ignore
