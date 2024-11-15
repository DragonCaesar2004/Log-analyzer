from dataclasses import dataclass
import re
from datetime import datetime
from src.config import LogFields

@dataclass
class LogObject: #TODO мб переделать в словарь для проверки в филтрах

    log_data   = {}

    def __init__(self, log_string: str) -> None:# TODO синхронизовать с конфигом
        # Регулярное выражение для распарсивания строки логов
        log_pattern = rf'''(?P<{LogFields.IP_ADDR.value}>\S+) - (?P<{LogFields.USER_NAME.value}>\S+) \[(?P<{LogFields.LOCAL_TIME.value}>.*?)\] "(?P<{LogFields.METHOD.value}>\S+) (?P<{LogFields.RESOURCE.value}>\S+) (?P<{LogFields.HTTP_VERSION.value}>[^"]+)" (?P<{LogFields.STATUS_CODE.value}>\d+) (?P<{LogFields.BODY_BYTES_SENT.value}>\d+) "(?P<{LogFields.HTTP_REFERER.value}>.*?)" "(?P<{LogFields.HTTP_USER_AGENT.value}>.*?)"'''
        match = re.match(log_pattern, log_string)
        if match:
            self.log_data[LogFields.IP_ADDR] = match.group(LogFields.IP_ADDR.value)
            self.log_data[LogFields.USER_NAME] = match.group(LogFields.USER_NAME.value)
            
            date_with_timezone = datetime.strptime(match.group(LogFields.LOCAL_TIME.value),'%d/%b/%Y:%H:%M:%S %z') 
            date_without_timezone= date_with_timezone.replace(tzinfo=None)

            self.log_data[LogFields.LOCAL_TIME] = date_without_timezone
             
            self.log_data[LogFields.METHOD] = match.group(LogFields.METHOD.value)
            self.log_data[LogFields.RESOURCE] = match.group(LogFields.RESOURCE.value)
            self.log_data[LogFields.HTTP_VERSION] = match.group(LogFields.HTTP_VERSION.value)

            self.log_data[LogFields.STATUS_CODE] = int(match.group(LogFields.STATUS_CODE.value))
            self.log_data[LogFields.BODY_BYTES_SENT] = int(match.group(LogFields.BODY_BYTES_SENT.value))
            self.log_data[LogFields.HTTP_REFERER] = match.group(LogFields.HTTP_REFERER.value)
            self.log_data[LogFields.HTTP_USER_AGENT] = match.group(LogFields.HTTP_USER_AGENT.value)
            

    def __getitem__(self,key):
        return self.log_data[key]
    
    def __str__(self):
        return self.log_data[LogFields.LOCAL_TIME].strftime("%Y-%m-%d %H:%M:%S")+'     '+ self.log_data[LogFields.METHOD]
 


