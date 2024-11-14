from dataclasses import dataclass
import re
from collections import defaultdict
from datetime import datetime

@dataclass
class LogObject: #TODO мб переделать в словарь для проверки в филтрах
    # ip_addr: str 
    # user_name: str 
    # local_time: str 
    # method: str 
    # status_code: int
    # body_bytes_sent: int
    # http_referer: str 
    # http_user_agent: str 
    log_data   = defaultdict()

    def __init__(self, log_string: str) -> None:# TODO синхронизовать с конфигом
        # Регулярное выражение для распарсивания строки логов
        log_pattern = r'(?P<ip_addr>\S+) - (?P<user_name>\S+) \[(?P<local_time>.*?)\] "(?P<method_info>.+?)" (?P<status_code>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)"'
        match = re.match(log_pattern, log_string)
        if match:
            self.log_data['ip_addr'] = match.group('ip_addr')
            self.log_data['user_name'] = match.group('user_name')
            
            date_with_timezone = datetime.strptime(match.group('local_time'),'%d/%b/%Y:%H:%M:%S %z') 

            date_without_timezone= date_with_timezone.replace(tzinfo=None)
            self.log_data['local_time'] = date_without_timezone
             
            method,resource,http_version = match.group('method_info').split()
            self.log_data['method'] = method
            self.log_data['resource'] = resource
            self.log_data['http_version'] = http_version
            
            self.log_data['status_code'] = int(match.group('status_code'))
            self.log_data['body_bytes_sent'] = int(match.group('body_bytes_sent'))
            self.log_data['http_referer'] = match.group('http_referer')
            self.log_data['http_user_agent'] = match.group('http_user_agent')

    def __getitem__(self,key):
        return self.log_data[key]
    
    def __str__(self):
        return self.log_data['local_time'].strftime("%Y-%m-%d %H:%M:%S")+'     '+ self.log_data['method']




