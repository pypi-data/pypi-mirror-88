from dataclasses import field
from typing import List

from ome_types.dataclasses import ome_dataclass


@ome_dataclass
class M:
    """This is a key/value pair used to build up a Mapping.

    The          Element and Attribute name are kept to single letters to minimize
    the          length at the expense of readability as they are likely to occur
    many          times.

    Parameters
    ----------
    k : str, optional
    """

    value: str
    k: str


@ome_dataclass
class Map:
    """This is a Mapping of key/value pairs.

    Parameters
    ----------
    k : str, optional
    m : M, optional
        This is a key/value pair used to build up a Mapping. The
        Element and Attribute name are kept to single letters to minimize the
        length at the expense of readability as they are likely to occur many
        times.
    """

    m: List[M] = field(default_factory=list)
