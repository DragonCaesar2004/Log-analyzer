import argparse
import urllib
import os
import urllib.parse
import re
from datetime import datetime
from typing import Optional
from glob import glob

from src.user_interfaces.base_user_interface import UserInterface
from src.project_types import InputArgs, AdressTypes, FormatTypes
from src.config import LogFields, one_argument_flags,description
from src.custom_exceptions import (
    NoFilesFoundError,
    UnknownArgumentsError,
    MissingPathError,
    InvalidPathError,
    InvalidDateFormatError,
    InvalidDateValueError,
    InvalidFormatStyleError,
    InvalidFilterFieldError,
    MissingFilterFieldError,
    DateOrderError,
    EmptyFilterValueError,
    EmptyArgumentError,
    MoreOneArgumentError,
     
)



class CommandLineInterface(UserInterface):
    '''
    Этот класс реализует интерфейс командной строки (CLI) для работы с логами. Он включает 
    в себя обработку входных аргументов, валидацию их значений и конвертацию в структуру данных для дальнейшей обработки. 
    '''
    def __init__(self)->None:
        '''Инициализирует парсер аргументов командной строки, добавляя параметры для анализа'''
        self.parser = argparse.ArgumentParser(
            prog="Анализатор логов", description=description,formatter_class=argparse.RawDescriptionHelpFormatter  
        )
        self.parser.add_argument(
            "-p", "--path", nargs="*", help="Путь: адрес URL или локального файла"
        )
        self.parser.add_argument(
            "--from-date", nargs="*", help="Время, С которого нужно начать фильтрацию"
        )
        self.parser.add_argument(
            "--to-date", nargs="*", help="Время, ДО которого нужно выполнить фильтрацию"
        )
        self.parser.add_argument(
            "--format", nargs="*", help="Формат времени для фильтрации"
        )
        self.parser.add_argument(
            "--filter-field",
            nargs="*",
            help="Поле, по которому будет происходить фильтрация",
        )
        self.parser.add_argument(
            "--filter-value", nargs="*", help="Значение поля для фильтрации"
        )

    def get_user_data(self) -> InputArgs:
        """
        Извлекает и проверяет аргументы командной строки, возвращая их в формате `InputArgs`.
        Ошибки:
            - UnknownArgumentsError: Если переданы неизвестные аргументы.
            - MissingPathError: Если отсутствует обязательный аргумент `-p` или `--path`.
            - InvalidPathError: Если путь не распознается как URL или локальный файл.
            - InvalidDateFormatError: Если формат даты не соответствует `YYYY-MM-DDThh:mm:ss`.
            - InvalidDateValueError: Если значение даты некорректно.
            - InvalidFormatStyleError: Если указан неизвестный стиль формата.
            - InvalidFilterFieldError: Если указано неизвестное поле фильтрации.
            - MissingFilterFieldError: Если значение фильтра задано без указания поля.
            - EmptyFilterValueError: Если значение фильтра пустое.
            - DateOrderError: Если начальная дата позже конечной.
        """

        args, unknown_args = self.parser.parse_known_args()
        return self._validate_args(args, unknown_args)

    def _validate_args(
        self, args: argparse.Namespace, unknown_args: list[str]
    ) -> InputArgs:
        """Валидирует аргументы заданные юзером"""
        self._validate_unknown_args(unknown_args)
        self._check_missing_params(args)
        self._check_one_argument(args)
         
        paths = self._deploy_file_paths(args.path)
        validated_paths = self._validate_path(paths)

        from_date = (
            self._validate_datetime_string(args.from_date) if args.from_date else None
        )
        to_date = self._validate_datetime_string(args.to_date) if args.to_date else None
        self._validate_date_order(from_date, to_date)
        
        format = self._validate_format_style(args.format) 
        
        filter_field = (
            self._validate_filter_field(args.filter_field)
            if args.filter_field
            else None
        )
        filter_value = (
            self._validate_filter_value(filter_field, args.filter_value)
        )
        
        return InputArgs(
            paths=validated_paths,
            from_date=from_date,
            to_date=to_date,
            format=format,
            filter_field=filter_field,
            filter_value=filter_value,
        )

    def _validate_unknown_args(self, unknown_args: list[str]) -> None:
        """  
        Проверяет наличие неизвестных аргументов.
        Ошибки:
            - UnknownArgumentsError: Если найдены неизвестные аргументы.
        """
        if len(unknown_args):
            raise UnknownArgumentsError(unknown_args)

    def _deploy_file_paths(self, paths: list[str])-> list[str]:
        '''
        Разворачивает пути из паттернов файлов.
        Ошибки:
            - NoFilesFoundError: Если файлы по шаблону не найдены.
             
        '''
        urls = []
        files = []
        file_patterns = []

        for path in paths:
            if self._is_url(path):
                urls.append(path)
            else:
                file_patterns.append(path)
         
        for file_pattern in file_patterns:
            try:
                deployed_files = glob(file_pattern, recursive=True)
                if  len(deployed_files) == 0:
                    raise ValueError
                files += deployed_files

            except ValueError as e:
                raise NoFilesFoundError(file_pattern) from e


        return files + urls

    def _validate_path(self, paths: list[str]) -> list[tuple[AdressTypes, str]]:
        """
        Проверяет корректность и тип указанных путей (файл или URL).
        Эта функция предназначена для проверки, является ли заданный путь URL-адресом,
        имеющим допустимый протокол.
                
        Ошибки:
            - MissingPathError: Если пути отсутствуют.
            - InvalidPathError: Если путь не является ни файлом, ни URL.
        """
         
        if not paths:
            raise MissingPathError()
        validated_paths :list[tuple[AdressTypes, str]]= []
        for path in paths:
            if self._is_url(path):
                validated_paths.append((AdressTypes.URL, path))
            elif self._is_file(path):
                validated_paths.append((AdressTypes.FILE, path))
            else:
                raise InvalidPathError(path)
        
        return validated_paths

    def _is_file(self, path: str) -> bool:
        """Проверяет является ли указанный локальный адрес файлом"""
        return os.path.isfile(path)

    def _is_url(self, path: str) -> bool:
        """Проверяет наличие протокола в пути"""
        parsed = urllib.parse.urlparse(path)
        return parsed.scheme in ["http", "https"]

    def _validate_datetime_string(self, date_list: list[str]) -> datetime:
        """
        Проверяет, что введеная дата соответствует формату YYYY-MM-DDThh:mm:ss и является валидной
        Ошибки:
            - InvalidDateFormatError: Если формат даты некорректен.
            - InvalidDateValueError: Если значение даты не распознается.
        """

        date_string = date_list[0]
        pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
        if not pattern.match(date_string):
            raise InvalidDateFormatError(date_string)
        try:
            return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise InvalidDateValueError()

    def _validate_format_style(self, format: str) -> FormatTypes:
        """
        Проверяет на наличие введеного формата в списке доступных стилей
        Ошибки:
            - InvalidFormatStyleError: Если формат не поддерживается.
        """
        if format is None:
            return FormatTypes.MARKDOWN.value # Markdown значение по умолчанию
        format_str = format[0]

        if format_str not in FormatTypes:
            raise InvalidFormatStyleError([format.value for format in FormatTypes])
        return FormatTypes(format_str)

    def _validate_filter_field(self, filter_field: str) ->LogFields:
        """
        Проверяет на наличие введеного фильтра в списке всех полей лога
        Ошибки:
            - InvalidFilterFieldError: Если поле не поддерживается.
        """
        filter_field_str = filter_field[0]
        if filter_field_str not in LogFields:
            raise InvalidFilterFieldError(LogFields)
        return LogFields(filter_field_str)

    def _validate_filter_value(
        self, filter_field: Optional[LogFields], filter_value: list[str]
    ) -> list[str]:
        """
        Проверка наличия значения у поля
        Ошибки:
            - MissingFilterFieldError: Если указано значение фильтра без поля.
            - EmptyFilterValueError: Если значение фильтра пустое.
        """
        if filter_field is None and filter_value is None:
            return None
        if filter_value is None:
            raise EmptyFilterValueError()

        if filter_field  is None and filter_value :
            raise MissingFilterFieldError()
        return filter_value

    def _validate_date_order(self, start_date: Optional[datetime], end_date: Optional[datetime])->None:
        """
        Проверяет, что начальная дата from_date раньше или равна конечной to_date.
        Ошибки:
            - DateOrderError: Если начальная дата позже конечной.
        """
        if start_date and end_date and start_date > end_date:
            raise DateOrderError()

    def _check_missing_params(self, args: argparse.Namespace) -> None:
        '''
        Проверяет, что у всех переданных аргументов есть значения.
        Ошибки:
            - EmptyArgumentError: Если аргумент задан, но пуст.
        '''
        for arg_name, arg_value in vars(args).items():
            if arg_value is None:
                continue
            if len(arg_value) == 0:
                raise EmptyArgumentError(arg_name)

    def _check_one_argument(self, args: argparse.Namespace)-> None:
        '''
        Проверяет, что для флагов, допускающих одно значение, передано не больше одного значения.
        Ошибки:
            - MoreOneArgumentError: Если передано больше одного значения.
        '''
        for arg_name, arg_value in vars(args).items():
            if arg_value is None:
                continue
            if arg_name in one_argument_flags and len(arg_value) > 1:
                raise MoreOneArgumentError(arg_name)
