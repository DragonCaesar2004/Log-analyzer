from typing import NamedTuple
from enum import Enum

class AdressTypes(Enum):
    URL='url'
    FILE='file'

        
class InputArgs(NamedTuple):
    # TODO
    adresses: ...
    from_date : ...# Optional
    to_date : ...# Optional
    format : ...# Optional
    filter_field : ...
    filter_value : ...


 