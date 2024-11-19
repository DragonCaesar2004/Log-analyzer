import pytest
import requests
from unittest.mock import patch, Mock
from src.log_object import LogObject
from src.custom_exceptions import HttpConectionError, ConnectionError
from src.parsers.url_parser import url_log_stream   

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get
 
def test_url_log_stream_success(mock_requests_get):
       mock_response = Mock()
       mock_response.status_code = 200
       mock_response.iter_lines.return_value = [
           b'127.0.0.1 - user [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "-" "Mozilla/5.0"',
           b'127.0.0.1 - user [10/Oct/2000:13:57:36 -0700] "GET /another_image.gif HTTP/1.0" 404 1234 "-" "Mozilla/5.0"'
       ]

       mock_requests_get.return_value.__enter__.return_value = mock_response

       log_generator = url_log_stream('http://example.com/logs')

       log_entry_1 = next(log_generator)
       log_entry_2 = next(log_generator)

       assert isinstance(log_entry_1, LogObject)
       assert isinstance(log_entry_2, LogObject)

       assert log_entry_1.ip_addr == '127.0.0.1'
       assert log_entry_1.user_name == 'user'
       assert log_entry_1.local_time.strftime("%d/%b/%Y:%H:%M:%S") == '10/Oct/2000:13:55:36'
       assert log_entry_1.method == 'GET'
       assert log_entry_1.resource == '/apache_pb.gif'
       assert log_entry_1.status_code == 200

       assert log_entry_2.ip_addr == '127.0.0.1'
       assert log_entry_2.user_name == 'user'
       assert log_entry_2.local_time.strftime("%d/%b/%Y:%H:%M:%S") == '10/Oct/2000:13:57:36'
       assert log_entry_2.method == 'GET'
       assert log_entry_2.resource == '/another_image.gif'
       assert log_entry_2.status_code == 404

def test_url_log_stream_connection_error(mock_requests_get):
    # Имитация ошибки соединения
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

    with pytest.raises(HttpConectionError):
        next(url_log_stream('http://example.com/logs'))

def test_url_log_stream_invalid_status(mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 500

    mock_requests_get.return_value.__enter__.return_value = mock_response

    with pytest.raises(ConnectionError):
        next(url_log_stream('http://example.com/logs'))