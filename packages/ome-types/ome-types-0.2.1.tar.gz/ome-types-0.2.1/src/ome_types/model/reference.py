from dataclasses import field
from typing import Any

from ome_types.dataclasses import ome_dataclass

from .simple_types import LSID


@ome_dataclass
class Reference:
    """Reference is an empty complex type that is contained and extended by all the
    *Ref elements and also the Settings Complex Type Each *Ref element defines an
    attribute named ID of simple type *ID and no other information Each simple
    type *ID is restricted to the base type LSID with an appropriate pattern
    """

    id: LSID
    ref_: Any = field(default=None, init=False)

    @property
    def ref(self) -> Any:
        if self.ref_ is None:
            raise ValueError("references not yet resolved on root OME object")
        return self.ref_()
