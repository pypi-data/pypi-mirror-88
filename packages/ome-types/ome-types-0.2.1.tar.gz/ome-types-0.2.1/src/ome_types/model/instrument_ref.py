from ome_types.dataclasses import EMPTY, ome_dataclass

from .reference import Reference
from .simple_types import InstrumentID


@ome_dataclass
class InstrumentRef(Reference):
    """This empty element can be used (via the required Instrument ID attribute) to
    refer to an Instrument defined within OME.

    Parameters
    ----------
    id : InstrumentID
    """

    id: InstrumentID = EMPTY  # type: ignore
