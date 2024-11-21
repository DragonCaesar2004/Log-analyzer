import re
from datetime import datetime

from src.config import LogFields
from src.custom_exceptions import LogNotMatchError


class LogObject:
    """
    Класс для представления и обработки объектов логов веб-сервера.

    Этот класс парсит строку лога с использованием регулярного выражения и
    устанавливает соответствующие атрибуты на основе найденных данных.
    """

    def __init__(self, log_string: str) -> None:
        """
        Инициализирует объект LogObject путем парсинга предоставленной строки лога.

        Использует регулярное выражение для извлечения различных полей из строки лога
        и устанавливает соответствующие атрибуты объекта. Если строка лога не соответствует
        ожидаемому формату, возбуждает исключение LogNotMatchError.

        Args:
            log_string (str): Строка лога для парсинга.

        Raises:
            LogNotMatchError: Если строка лога не соответствует ожидаемому формату.
        """

        # Регулярное выражение для распарсивания строки логов
        log_pattern = rf'''(?P<{LogFields.IP_ADDR.value}>\S+) - (?P<{LogFields.USER_NAME.value}>\S+) \[(?P<{LogFields.LOCAL_TIME.value}>.*?)\] "(?P<{LogFields.METHOD.value}>\S+) (?P<{LogFields.RESOURCE.value}>\S+) (?P<{LogFields.HTTP_VERSION.value}>[^"]+)" (?P<{LogFields.STATUS_CODE.value}>\d+) (?P<{LogFields.BODY_BYTES_SENT.value}>\d+) "(?P<{LogFields.HTTP_REFERER.value}>.*?)" "(?P<{LogFields.HTTP_USER_AGENT.value}>.*?)"'''
        match = re.match(log_pattern, log_string)
        if match:
            # инициализация через setattr для синхронизации данных,
            setattr(self, LogFields.IP_ADDR.value, match.group(LogFields.IP_ADDR.value))
            setattr(
                self, LogFields.USER_NAME.value, match.group(LogFields.USER_NAME.value)
            )

            date_with_timezone = datetime.strptime(
                match.group(LogFields.LOCAL_TIME.value), "%d/%b/%Y:%H:%M:%S %z"
            )
            date_without_timezone = date_with_timezone.replace(tzinfo=None)
            setattr(self, LogFields.LOCAL_TIME.value, date_without_timezone)

            setattr(self, LogFields.METHOD.value, match.group(LogFields.METHOD.value))
            setattr(
                self, LogFields.RESOURCE.value, match.group(LogFields.RESOURCE.value)
            )
            setattr(
                self,
                LogFields.HTTP_VERSION.value,
                match.group(LogFields.HTTP_VERSION.value),
            )
            setattr(
                self,
                LogFields.STATUS_CODE.value,
                int(match.group(LogFields.STATUS_CODE.value)),
            )
            setattr(
                self,
                LogFields.BODY_BYTES_SENT.value,
                int(match.group(LogFields.BODY_BYTES_SENT.value)),
            )
            setattr(
                self,
                LogFields.HTTP_REFERER.value,
                match.group(LogFields.HTTP_REFERER.value),
            )
            setattr(
                self,
                LogFields.HTTP_USER_AGENT.value,
                match.group(LogFields.HTTP_USER_AGENT.value),
            )
        else:
            raise LogNotMatchError(log_string)

    def __eq__(self, other: object) -> bool:
        """
        Данный dunder метод определён для сравненния логов по их соответствующим артриутам.
        Он необходим только для тестирования
        """
        if not isinstance(other, LogObject):
            """Если объекты сравнения имеют разный тип, сразу выкидываем исключение"""
            raise TypeError(f"Нельзя сравнить LogObject с {type(other).__name__}")

        return (
            getattr(self, LogFields.IP_ADDR.value)
            == getattr(other, LogFields.IP_ADDR.value)
            and getattr(self, LogFields.USER_NAME.value)
            == getattr(other, LogFields.USER_NAME.value)
            and getattr(self, LogFields.LOCAL_TIME.value)
            == getattr(other, LogFields.LOCAL_TIME.value)
            and getattr(self, LogFields.METHOD.value)
            == getattr(other, LogFields.METHOD.value)
            and getattr(self, LogFields.RESOURCE.value)
            == getattr(other, LogFields.RESOURCE.value)
            and getattr(self, LogFields.HTTP_VERSION.value)
            == getattr(other, LogFields.HTTP_VERSION.value)
            and getattr(self, LogFields.STATUS_CODE.value)
            == getattr(other, LogFields.STATUS_CODE.value)
            and getattr(self, LogFields.BODY_BYTES_SENT.value)
            == getattr(other, LogFields.BODY_BYTES_SENT.value)
            and getattr(self, LogFields.HTTP_REFERER.value)
            == getattr(other, LogFields.HTTP_REFERER.value)
            and getattr(self, LogFields.HTTP_USER_AGENT.value)
            == getattr(other, LogFields.HTTP_USER_AGENT.value)
        )
