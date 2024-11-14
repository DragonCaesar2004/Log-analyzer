import argparse
import urllib
import os
import urllib.parse
import re
from datetime import datetime
from typing import Optional
from src.custom_exceptions import UnknownArgumentsError, MissingPathError, InvalidPathError, InvalidDateFormatError, InvalidDateValueError, InvalidFormatStyleError, InvalidFilterFieldError, MissingFilterFieldError, EmptyFilterValueError, DateOrderError, EmptyArgumentError, MoreOneArgumentError


from src.user_interfaces.base_user_interface import UserInterface
from src.project_types import InputArgs
from src.config import formats, log_fields, one_argument_flags

class CommandLineInterface(UserInterface):

    def get_init_data(self)-> InputArgs | Exception:
        """
        Анализирует и проверяет аргументы командной строки.

        :raises UnknownArgumentsError: Если переданы неизвестные аргументы.
        :raises MissingPathError: Если отсутствует обязательный аргумент -p / --path: URL или адрес локального файла.
        :raises InvalidPathError: Если путь не может быть распознан как файл или URL.
        :raises InvalidDateFormatError: Если формат даты неверный.
        :raises InvalidDateValueError: Если значение даты некорректно.
        :raises InvalidFormatStyleError: Если указан неизвестный формат стиля.
        :raises InvalidFilterFieldError: Если указано неизвестное поле фильтрации.
        :raises MissingFilterFieldError: Если значение фильтра указано без поля.
        :raises EmptyFilterValueError: Если значение фильтра пусто и необходим плейсхолдер.
        """
        parser = self._init_parser()
        args, unknown_args = parser.parse_known_args()
        return self._validate_args(args, unknown_args)

    def _init_parser(self) -> argparse.ArgumentParser:
        """Инициализирует и возвращает объект парсера."""
        parser = argparse.ArgumentParser(prog='Анализатор логов', description='Описание ДОБАВИТЬ')

        parser.add_argument( '-p', '--path', nargs='*', help='Путь: адрес URL или локального файла')
        parser.add_argument('--from-date', nargs='*', help='Время, С которого нужно начать фильтрацию')
        parser.add_argument('--to-date', nargs='*', help='Время, ДО которого нужно выполнить фильтрацию')
        parser.add_argument('--format', nargs='*', help='Формат времени для фильтрации')
        parser.add_argument('--filter-field',nargs='*', help='Поле, по которому будет происходить фильтрация')
        parser.add_argument( '--filter-value', nargs='*', help='Значение поля для фильтрации')
        return parser

    def _validate_args(self, args: argparse.Namespace, unknown_args: list[str]) -> InputArgs:
        """Валидирует аргументы заданные юзером"""
        self._validate_unknown_args(unknown_args)
        self._check_missing_params(args)
        #  проверить в цикле флаги на наличе определённого числа параметров
        
        self._check_one_argument(args)
        urls, files = self._validate_path(args.path)
        from_date = self._validate_datetime_string(args.from_date) if args.from_date else None
        to_date = self._validate_datetime_string(args.to_date) if args.to_date else None
        self._validate_date_order(from_date,to_date)

        format = self._validate_format_style(args.format)  if args.format else None
        
        filter_field = self._validate_filter_field(args.filter_field) if args.filter_field else None
        filter_value = self._validate_filter_value(filter_field, args.filter_value) if filter_field else None
        
        return InputArgs(urls=urls, files=files, from_date=from_date, to_date=to_date, format=format, filter_field=filter_field, filter_value=filter_value)

    def _validate_unknown_args(self, unknown_args: list[str]) -> None:
        """Проверяет наличие неизвестных аргументов"""
        if len(unknown_args):
            raise UnknownArgumentsError(unknown_args)

    def _validate_path(self, paths: Optional[list[str]]) -> tuple[list[str], list[str]]:
        """Разделяет на 2 списка url и файлы. Возвращает их 
        Эта функция предназначена для проверки, является ли заданный путь URL-адресом, 
        имеющим допустимый протокол. """
        if not paths:
            raise MissingPathError()
        urls, files = [], []
        for path in paths:
            if self._is_url(path):
                urls.append(path)
            elif self._is_file(path):
                files.append(path)
            else:
                raise InvalidPathError(path)
        return urls, files

    def _is_file(self, path: str) -> bool:
        """Проверяет вляется ли указанный локальный адрес файлом"""
        return os.path.isfile(path)

    def _is_url(self, path: str) -> bool:
        """Проверяет наличие протокола в пути""" #TODO дописать
        parsed = urllib.parse.urlparse(path)
        return parsed.scheme in ['http', 'https']

    # TODO
    def _validate_datetime_string(self, date_list: list[str]) -> datetime:
        """Проверяет, что введеная дата соответствует формату YYYY-MM-DDThh:mm:ss и является валидной"""
        
        date_string = date_list[0]
        pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
        if not pattern.match(date_string):
            raise InvalidDateFormatError(date_string)
        try:
            return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise InvalidDateValueError()

    def _validate_format_style(self, format: str) :
        """Проверяет на наличие введеного формата в списке доступных стилей"""
        format_str = format[0]
        if format_str not in formats:
            raise InvalidFormatStyleError( formats)
        return format_str

    def _validate_filter_field(self, filter_field: str) -> None:
        """Проверяет на наличие введеного фильтра в списке всех полей лога"""
        filter_field_str = filter_field[0]
        if filter_field_str not in log_fields:
            raise InvalidFilterFieldError( log_fields)
        return filter_field_str

    def _validate_filter_value(self, filter_field: str, filter_value: Optional[list[str]]) -> None:
        """Проверка наличия значения у поля """
        if not filter_field:
            raise MissingFilterFieldError()
        if not filter_value:
            raise EmptyFilterValueError()
        
        return filter_value
    
    def _validate_date_order(self,start_date: datetime, end_date: datetime):
        """
        Проверяет, что start_date раньше end_date.

        :param start_date: Начальная дата.
        :param end_date: Конечная дата.
        :raises DateOrderError: Если start_date позже или равна end_date.
        """
        if start_date and end_date:
            if start_date > end_date:
                raise DateOrderError()

    def _check_missing_params(self, args):
        for arg_name, arg_value in vars(args).items():
            if arg_value is None: 
                continue
            if len(arg_value)==0:
                raise EmptyArgumentError(arg_name)
    def _check_one_argument(self, args):        
        for arg_name, arg_value in vars(args).items():
            if arg_value is None: 
                continue
            if arg_name in one_argument_flags and len(arg_value)>1:
                raise MoreOneArgumentError(arg_name)