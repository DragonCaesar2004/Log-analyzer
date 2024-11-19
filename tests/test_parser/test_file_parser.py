import pytest
from unittest.mock import mock_open, patch
from src.log_object import LogObject
from src.custom_exceptions import ReadFileError
from src.parsers.file_parser import file_log_stream   


def test_file_log_stream_success():
    # Создаем тестовые данные
    mock_data = '''178.30.216.251 - - [09/Nov/2024:15:08:29 +0000] "GET /structure.js HTTP/1.1" 200 2115 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/531.11.7 (KHTML, like Gecko) Version/5.2 Safari/531.11.7"\n
183.75.122.0 - - [09/Nov/2024:15:08:30 +0000] "GET /data-warehouse-Synchronised/optimal/initiative-monitoring.png HTTP/1.1" 200 952 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:7.0) Gecko/1962-29-04 Firefox/36.0"'''


    # Используем mock_open для имитации открытия файла
    with patch("builtins.open", mock_open(read_data=mock_data)):
        generator = file_log_stream("fake_path.log")
        
        # Преобразуем генератор в список для проверки
        logs = list(generator)

    # Проверяем, что возвращаются объекты LogObject и содержимое корректно
    assert len(logs) == 2
    assert logs[0] == LogObject('178.30.216.251 - - [09/Nov/2024:15:08:29 +0000] "GET /structure.js HTTP/1.1" 200 2115 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/531.11.7 (KHTML, like Gecko) Version/5.2 Safari/531.11.7"')
    assert logs[1] == LogObject( '183.75.122.0 - - [09/Nov/2024:15:08:30 +0000] "GET /data-warehouse-Synchronised/optimal/initiative-monitoring.png HTTP/1.1" 200 952 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:7.0) Gecko/1962-29-04 Firefox/36.0"')
 

def test_file_log_stream_empty_file():
    # Пустой файл
    mock_data = ""

    with patch("builtins.open", mock_open(read_data=mock_data)):
        generator = file_log_stream("fake_path.log")
        logs = list(generator)

    # Проверяем, что возвращается пустой список
    assert logs == []

def test_file_log_stream_file_not_found():
    # Тестируем обработку ошибки файла
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(ReadFileError):
            list(file_log_stream("fake_path.log"))
