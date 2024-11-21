import pytest
from collections import Counter
from src.log_statistics_processor import LogStatisticsProcessor
from src.log_object import LogObject


@pytest.fixture
def log_processor():
    # Инициализация LogStatisticsProcessor перед каждым тестом
    processor = LogStatisticsProcessor()
    return processor


@pytest.fixture(scope="session")
def logs():
    logs = [
        LogObject(
            '127.0.0.1 - user [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "-" "Mozilla/5.0"'
        ),
        LogObject(
            '127.0.0.1 - - [17/May/2015:08:05:23 +0000] "GET /downloads/product_1 HTTP/1.1" 304 230 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"'
        ),
        LogObject(
            '80.91.33.133 - - [17/May/2015:08:05:24 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.17)"'
        ),
    ]
    return logs


def test_init(log_processor):
    assert log_processor.logs_count == 0
    assert isinstance(log_processor.resource_frequency, Counter)
    assert isinstance(log_processor.status_code_frequency, Counter)
    assert log_processor.weights_all_logs == []
    assert log_processor.unique_users == set()


def test_calculate_statistics_with_single_entry(log_processor):
    log = LogObject(
        '127.0.0.1 - user [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "-" "Mozilla/5.0"'
    )
    log_processor.calculate_statistics(log)
    assert log_processor.logs_count == 1
    assert log_processor.resource_frequency["/apache_pb.gif"] == 1
    assert log_processor.status_code_frequency[200] == 1
    assert log_processor.weights_all_logs == [2326]
    assert log_processor.unique_users == {"127.0.0.1"}


def test_calculate_statistics_with_multiple_entries(log_processor, logs):

    for log in logs:
        log_processor.calculate_statistics(log)
    assert log_processor.logs_count == 3
    assert log_processor.resource_frequency["/apache_pb.gif"] == 1
    assert log_processor.resource_frequency["/downloads/product_1"] == 2
    assert log_processor.status_code_frequency[200] == 1
    assert log_processor.status_code_frequency[304] == 2
    assert log_processor.weights_all_logs == [2326, 230, 0]
    assert log_processor.unique_users == {"127.0.0.1", "80.91.33.133"}


def test_calculate_percentile(log_processor, logs):

    for log in logs:
        log_processor.calculate_statistics(log)
    percentile = log_processor._calculate_percentile()
    assert (
        percentile == 230
    )  # 95% перцентиль, т.к. отсортировано [0, 230, 2326] - это будет 200


def test_get_statistics(log_processor, logs):
    logs = [
        LogObject(
            '127.0.0.1 - user [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "-" "Mozilla/5.0"'
        ),
        LogObject(
            '127.0.0.1 - - [17/May/2015:08:05:23 +0000] "GET /downloads/product_1 HTTP/1.1" 304 230 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"'
        ),
        LogObject(
            '80.91.33.133 - - [17/May/2015:08:05:24 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.17)"'
        ),
    ]
    for log in logs:
        log_processor.calculate_statistics(log)
    statistics = log_processor.get_statistics()
    assert statistics.logs_count == 3
    assert statistics.unique_users_number == 2  # три уникальных пользователя
    assert statistics.average_response_size == 852.0
    assert statistics.resource_frequency["/downloads/product_1"] == 2
    assert statistics.status_code_frequency[200] == 1
    assert statistics.status_code_frequency[304] == 2


# Запуск тестов из командной строки
# Для запуска тестов просто выполните команду `pytest` в терминале в каталоге, где находятся ваши тесты.
