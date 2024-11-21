from typing import NamedTuple, Optional
from enum import Enum
from datetime import datetime
from collections import Counter

from src.config import LogFields


class AdressTypes(Enum):
    """
    Перечисление типов адресов для ввода.

    Атрибуты:
        URL (str): Тип адреса, представляющий URL.
        FILE (str): Тип адреса, представляющий путь к файлу.
    """

    URL: str = "url"
    FILE: str = "file"


class FormatTypes(Enum):
    """
    Перечисление типов форматов для вывода результатов.

    Атрибуты:
        MARKDOWN (str): Формат Markdown.
        ADOC (str): Формат AsciiDoc.
    """

    MARKDOWN: str = "md"
    ADOC: str = "adoc"


class InputArgs(NamedTuple):
    """
    Именнованный ортеж для хранения аргументов ввода.

    Атрибуты:
        paths (List[Tuple[AdressTypes, str]]): Список путей, где каждый путь представлен кортежем типа адреса и строки.
        from_date (Optional[datetime]): Начальная дата для фильтрации логов. Может быть None.
        to_date (Optional[datetime]): Конечная дата для фильтрации логов. Может быть None.
        format (FormatTypes): Формат вывода статистики.
        filter_field (Optional[LogFields]): Поле лога для фильтрации. Может быть None.
        filter_value (List[str]): Список значений для фильтрации по указанному полю.
    """

    paths: list[tuple[AdressTypes, str]]
    from_date: Optional[datetime]
    to_date: Optional[datetime]
    format: FormatTypes
    filter_field: Optional[LogFields]
    filter_value: Optional[list[str]]


class LogStatistics(NamedTuple):
    """
    Кортеж для хранения статистики логов.

    Атрибуты:
        logs_count (int): Общее количество обработанных логов.
        resource_frequency (Counter): Частота обращения к различным ресурсам.
        status_code_frequency (Counter): Частота различных HTTP-статусов.
        percentile (int): Перцентиль для анализа, например, 95.
        unique_users_number (int): Количество уникальных пользователей.
        average_response_size (float): Средний размер ответа в байтах.
    """

    logs_count: int
    resource_frequency: Counter
    status_code_frequency: Counter
    percentile: int
    unique_users_number: int
    average_response_size: float
