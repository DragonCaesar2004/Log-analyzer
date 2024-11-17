from enum import Enum

percentile_ratio = 0.95

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
