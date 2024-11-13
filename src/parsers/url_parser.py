import requests  
from typing import Generator  

from src.parsers.log_parser import LogParser
from src.log_object import LogObject
from src.custom_exceptions import HttpConectionError

class UrlParser(LogParser):
    """
    Класс UrlParser, который наследует от LogParser и обеспечивает возможность
    потоковой обработки логов NGINX, доступных по URL.
    """
    
    def log_stream(self, url: str) -> Generator[LogObject, None, None]:
        '''
        Функция для выполнения потоковой обработки данных из файла логов NGINX по URL.
        
        Аргументы:
            url (str): URL файла логов NGINX.
        
        Возвращает:
            Generator[LogObject, None, None]: Генератор, возвращающий объекты LogObject,
            представляющие распарсенные записи лога.
        '''
        try:
            # Отправляем GET-запрос для извлечения содержимого файла логов. 
            # Указываем параметр stream=True, чтобы получать данные по мере их загрузки.
            with requests.get(url, stream=True) as response:
                # Проверяем наличие ошибок HTTP (например, 404, 500 и т.д.).
                if response.status_code != 200:
                # Если код состояния не 200, выбрасываем собственное исключение.
                    raise ConnectionError(f"Получен неверный код состояния: {response.status_code}") 
                
                # Перебираем каждую строку в ответе, используя метод iter_lines(),
                # который позволяет итерироваться по строкам в потоке данных.
                for line in response.iter_lines():
                    if line:  # Проверяем, что строка не пустая
                        # Преобразуем байтовую строку в строку с использованием UTF-8
                        log_line = line.decode('utf-8')

                        # Здесь предполагается, что нужно разобрать строку лога на объект LogObject.
                        # (Измените на нужное преобразование, если требуется)
                        # Вернем с помощью yield лог-строку как LogObject.
                        yield LogObject(log_line)  # Создается объект LogObject с данным логом
        except requests.exceptions.RequestException as e:
            # В случае возникновения исключения при выполнении запроса,
            # поднимаем ValueError с сообщением об ошибке.
            raise HttpConectionError(url) from e # TODO
