from dataclasses import field
from typing import List

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .manufacturer_spec import ManufacturerSpec
from .simple_types import DichroicID


@ome_dataclass
class Dichroic(ManufacturerSpec):
    """The dichromatic beamsplitter or dichroic mirror used for this filter
    combination.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    id : DichroicID
    lot_number : str, optional
        The lot number of the component.
    manufacturer : str, optional
        The manufacturer of the component.
    model : str, optional
        The Model of the component.
    serial_number : str, optional
        The serial number of the component.
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    id: DichroicID = AUTO_SEQUENCE  # type: ignore
