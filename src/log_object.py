import re
from datetime import datetime

from src.config import LogFields


class LogObject:

    def __init__(self, log_string: str) -> None:
        # Регулярное выражение для распарсивания строки логов
        log_pattern = rf'''(?P<{LogFields.IP_ADDR.value}>\S+) - (?P<{LogFields.USER_NAME.value}>\S+) \[(?P<{LogFields.LOCAL_TIME.value}>.*?)\] "(?P<{LogFields.METHOD.value}>\S+) (?P<{LogFields.RESOURCE.value}>\S+) (?P<{LogFields.HTTP_VERSION.value}>[^"]+)" (?P<{LogFields.STATUS_CODE.value}>\d+) (?P<{LogFields.BODY_BYTES_SENT.value}>\d+) "(?P<{LogFields.HTTP_REFERER.value}>.*?)" "(?P<{LogFields.HTTP_USER_AGENT.value}>.*?)"'''
        match = re.match(log_pattern, log_string)
        if match:
            # инициализация через setattr для синхронизации данных
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
