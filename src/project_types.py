from typing import NamedTuple


class InputArgs(NamedTuple):
    # TODO
    urls: list[str]
    files: list[str]
    from_date : ...# Optional
    to_date : ...# Optional
    format : ...# Optional
    filter_field : ...
    filter_value : ...


 