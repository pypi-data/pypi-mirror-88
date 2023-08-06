from dataclasses import field
from typing import Any, Dict, List, Optional, Union

from pydantic import validator

from ome_types.dataclasses import AUTO_SEQUENCE, ome_dataclass

from .annotation_ref import AnnotationRef
from .ellipse import Ellipse
from .label import Label
from .line import Line
from .mask import Mask
from .point import Point
from .polygon import Polygon
from .polyline import Polyline
from .rectangle import Rectangle
from .shape import Shape
from .simple_types import ROIID

_shape_types: Dict[str, type] = {
    "point": Point,
    "line": Line,
    "rectangle": Rectangle,
    "ellipse": Ellipse,
    "polyline": Polyline,
    "polygon": Polygon,
    "mask": Mask,
    "label": Label,
}


@ome_dataclass
class ROI:
    """A four dimensional 'Region of Interest'.

    If they are not used, and the Image has more than one plane, the entire set of
    planes is assumed to be included in the ROI. Multiple ROIs may be specified.

    Parameters
    ----------
    annotation_ref : AnnotationRef, optional
    description : str, optional
        A description for the ROI.
    id : ROIID
    name : str, optional
        The Name identifies the ROI to the user.
    union : List[Shape], optional
    """

    annotation_ref: List[AnnotationRef] = field(default_factory=list)
    description: Optional[str] = None
    id: ROIID = AUTO_SEQUENCE  # type: ignore
    name: Optional[str] = None
    union: List[Shape] = field(default_factory=list)

    @validator("union", pre=True, each_item=True)
    def validate_union(cls, value: Union[Shape, Dict[Any, Any]]) -> Shape:
        if isinstance(value, Shape):
            return value
        elif isinstance(value, dict):
            try:
                _type = value.pop("_type")
            except KeyError:
                raise ValueError("dict initialization requires _type") from None
            try:
                shape_cls = _shape_types[_type]
            except KeyError:
                raise ValueError(f"unknown Shape type '{_type}'") from None
            return shape_cls(**value)
        else:
            raise ValueError("invalid type for union values")
