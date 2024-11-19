from enum import Enum

percentile_ratio:float = 0.95 

one_argument_flags = ("from_date", "to_date", "format", "filter_field")


class LogFields(Enum):
    IP_ADDR = "ip_addr"
    USER_NAME = "user_name"
    LOCAL_TIME = "local_time"
    METHOD = "method"
    RESOURCE = "resource"
    HTTP_VERSION = "http_version"
    STATUS_CODE = "status_code"
    BODY_BYTES_SENT = "body_bytes_sent"
    HTTP_REFERER = "http_referer"
    HTTP_USER_AGENT = "http_user_agent"

description = '''На вход программе через аргументы командной строки задаётся:
1. Путь к одному или нескольким NGINX лог-файлам в виде локального шаблона или URL.
2. Необязательные временные параметры from и to в формате ISO8601.
3. Необязательный параметр формата вывода результата: markdown или adoc.

Функции программы:
- Подсчитывает общее количество запросов.
- Определяет наиболее часто запрашиваемые ресурсы.
- Определяет наиболее часто встречающиеся коды ответа.
- Рассчитывает средний размер ответа сервера.
- Рассчитывает 95% перцентиль размера ответа сервера.
'''
