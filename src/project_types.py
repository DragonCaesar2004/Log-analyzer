from typing import NamedTuple, Optional
from enum import Enum
from datetime import datetime
from collections import Counter

from src.config import LogFields

class AdressTypes(Enum):
    URL: str = "url"
    FILE: str = "file"


class FormatTypes(Enum):
    MARKDOWN: str = "md"
    ADOC: str = "adoc"


class InputArgs(NamedTuple):
    paths: list[tuple[AdressTypes,str]]
    from_date: Optional[datetime]
    to_date: Optional[datetime]  
    format: FormatTypes
    filter_field: Optional[LogFields]
    filter_value: list[str]


class LogStatistics(NamedTuple):
    logs_count: int
    resource_frequency: Counter
    status_code_frequency: Counter
    percentile: int
    unique_users_number: int
    average_response_size: float
