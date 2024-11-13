from dataclasses import dataclass
import re

@dataclass
class LogObject:
    ip_addr: str = ''
    user_name: str = '-'
    local_time: str = ''
    method: str = ''
    status_code: int = 0
    body_bytes_sent: int = 0
    http_referer: str = '-'
    http_user_agent: str = ''

    def __init__(self, log_string: str) -> None:# TODO синхронизовать с конфигом
        # Регулярное выражение для распарсивания строки логов
        log_pattern = r'(?P<ip_addr>\S+) - (?P<user_name>\S+) \[(?P<local_time>.*?)\] "(?P<method>.+?)" (?P<status_code>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>.*?)" "(?P<http_user_agent>.*?)"'
        match = re.match(log_pattern, log_string)
        if match:
            self.ip_addr = match.group('ip_addr')
            self.user_name = match.group('user_name')
            self.local_time = match.group('local_time')
            self.method = match.group('method')
            self.status_code = int(match.group('status_code'))
            self.body_bytes_sent = int(match.group('body_bytes_sent'))
            self.http_referer = match.group('http_referer')
            self.http_user_agent = match.group('http_user_agent')