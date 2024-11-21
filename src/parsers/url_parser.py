import requests
from typing import Generator


from src.log_object import LogObject
from src.custom_exceptions import HttpConectionError, ConnectionError


def url_log_stream(path: str) -> Generator[LogObject, None, None]:
    """
    Функция для выполнения потоковой обработки данных из файла логов NGINX по path.

    Аргументы:
        path (str): path файла логов NGINX.

    Возвращает:
        Generator[LogObject, None, None]: Генератор, возвращающий объекты LogObject,
        представляющие распарсенные записи лога.
    """
    try:

        # Отправляем GET-запрос для извлечения содержимого файла логов.
        # Указываем параметр stream=True, чтобы получать данные по мере их загрузки.
        with requests.get(path, stream=True, timeout=10) as response:
            if response.status_code != 200:
                raise ConnectionError(response.status_code)

            # Перебираем каждую строку в ответе, используя метод iter_lines()
            for line in response.iter_lines():
                if line:
                    # Преобразуем байтовую строку в обычную с использованием UTF-8
                    log_line = line.decode("utf-8")

                    yield LogObject(log_line)
    except requests.exceptions.RequestException as e:
        raise HttpConectionError(path) from e
