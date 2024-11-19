from src.log_object import LogObject
import pytest

def test_init_log_obj():
    log_obj = LogObject( '127.0.0.1 - user [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "-" "Mozilla/5.0"')
    print(log_obj)
    print(type(log_obj))
    assert log_obj.ip_addr == '127.0.0.1'
    assert log_obj.user_name == 'user'
    assert log_obj.local_time.strftime("%Y-%m-%d %H:%M:%S") == '2000-10-10 13:55:36'
    assert log_obj.method == 'GET'
    assert log_obj.resource == '/apache_pb.gif'
    assert log_obj.http_version == 'HTTP/1.0'
    assert log_obj.status_code == 200
    assert log_obj.body_bytes_sent == 2326
    assert log_obj.http_referer == '-'
    assert log_obj.http_user_agent == 'Mozilla/5.0'


def test_wrong_equal():
    log_obj = LogObject( '127.0.0.1 - user [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "-" "Mozilla/5.0"')
    with pytest.raises(TypeError):
        log_obj == 1