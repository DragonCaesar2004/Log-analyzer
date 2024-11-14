import requests

class UnknownArgumentsError(Exception):
    '''Вызывается, если были переданы неизвестные аргументы.'''
    def __init__(self, unknown_args: list[str]):
        super().__init__(f'Ошибка. Вы ввели неизвестные параметры: {' '.join(unknown_args)}')

class MissingPathError(Exception):
    '''Вызывается, если отсутствует обязательный аргумент -p / --path: URL или адрес локального файла.'''
    def __init__(self):
        super().__init__('Ошибка: Отсутствует обязательный аргумент -p / --path: URL или адрес локального файла')

class InvalidPathError(Exception):
    '''Вызывается, если путь не может быть распознан как файл или URL.'''
    def __init__(self, path: str):
        super().__init__(f'Путь {path} не распознан')

class InvalidDateFormatError(ValueError):
    '''Вызывается, если формат даты не соответствует ожидаемому.'''
    def __init__(self, date_string: str):
        super().__init__(f'Ошибка: не соответствие формату времени. Введите дату в таком формате: YYYY-MM-DDThh:mm:ss (введено: {date_string})')

class FlagWithoutValueError(Exception):
    '''Вызывается, если пользователь использовал флаг без параметров,хотя они нужны''' 
    def __init__(self, flag_name):
        super().__init__(f'Использован флаг {flag_name}, но без параметров')

class InvalidDateValueError(ValueError):
    '''Вызывается, если указано неверное значение для времени.'''
    def __init__(self):
        super().__init__('Ошибка: указано неверное значение для времени')

class InvalidFormatStyleError(ValueError):
    '''Вызывается, если указан неизвестный формат стиля.'''
    def __init__(self, allowed_formats: list[str]):
        super().__init__(f'Ошибка: выберите один из следующих форматов: {', '.join(allowed_formats)}')

class InvalidFilterFieldError(ValueError):
    '''Вызывается, если указано неизвестное поле фильтрации.'''
    def __init__(self, allowed_fields: list[str]):
        super().__init__(f'Ошибка: выберите одно из следующих полей для фильтрации: {', '.join(allowed_fields)}')

class MissingFilterFieldError(ValueError):
    '''Вызывается, если значение фильтра указано без поля.'''
    def __init__(self):
        super().__init__('Ошибка: Вы не указали поле для фильтрации')

class EmptyFilterValueError(ValueError):
    '''Вызывается, если значение фильтра пусто, .'''
    def __init__(self):
        super().__init__('Ошибка: Вы не выбрали значение для фильтрации. Напишите его после флага --filter-value')

class HttpConectionError(requests.exceptions.RequestException):
    '''Вызывается, если не удалось подключиться к указанному URL'''
    def __init__(self,url:str):
        super().__init__(f'Не удалось подключиться к : {url}')

class DateOrderError(ValueError): # Переименовать 
    '''Вызывается, когда время, с которого надо начать поиск позже, времени до которого нужно осуществить поиск'''
    def __init__(self):
        super().__init__('Время, с которого надо начать поиск позже, времени до которого нужно осуществить поиск')


class EmptyArgumentError(ValueError):
    '''Вызывается, если значение фильтра пусто, .'''
    def __init__(self,flag:str):
        super().__init__(f'Ошибка: Вы указали пустой аргумент для флага {flag}')

class MoreOneArgumentError(ValueError):
    def __init__(self, flag:str):
        super().__init__(f'Указано больше 1 аргумента для флага {flag}')