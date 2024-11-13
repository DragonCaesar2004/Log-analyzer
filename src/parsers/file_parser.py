 
from typing import Generator

from src.parsers.log_parser import LogParser
from src.log_object import LogObject

class FileParser(LogParser):
    """
    Класс FileParser, который наследует от LogParser и обеспечивает возможность
    потоковой обработки логов NGINX из локального файла.
    """

    def log_stream(self, path: str) -> Generator[LogObject, None, None]:
        '''
        Функция для выполнения потоковой обработки данных из локального файла логов NGINX.
        
        Аргументы:
            path (str): Путь к файлу логов NGINX.
        
        Возвращает:
            Generator[LogObject, None, None]: Генератор, возвращающий объекты LogObject,
            представляющие распарсенные записи лога.
        '''
        try:
                     
            # Открываем файл в режиме чтения с указанием кодировки UTF-8
            with open(path, 'r', encoding='utf-8') as file:
                # Итерируемся по строкам файла
                for line in file:
                    if line.strip():  # Проверяем, что строка не пустая после удаления пробелов
                        # Создаем объект LogObject из строки лога
                        yield LogObject(line.strip())
        except Exception as e:
            # В случае ошибки при чтении файла выбрасываем исключение с описанием проблемы
            raise ValueError(f"Произошла ошибка при чтении файла логов: {e}") from e
