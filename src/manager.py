from typing import assert_never

from src.project_types import InputArgs, AdressTypes, FormatTypes
from src.parsers.url_parser import url_log_stream
from src.parsers.file_parser import file_log_stream
from src.log_object import LogObject
from src.log_statistics_processor import LogStatisticsProcessor
from src.report_creator import BaseReportCreator


class Manager:
    """
    Manager отвечает за обработку данных журналов из различных источников, применение фильтров,
    вычисление статистики и генерацию отчетов в указанном формате.

    Атрибуты:
        input_args (InputArgs): Входные аргументы, содержащие пути, формат и параметры фильтрации.
        log_statistics_processor (LogStatisticsProcessor): Процессор для вычисления статистики журналов.
    """

    def __init__(self, input_args: InputArgs) -> None:
        self.input_args = input_args
        self.log_statistics_processor = LogStatisticsProcessor()

    def create_report_content(self) -> None:
        """
        Обрабатывает данные журналов из указанных источников, применяет фильтры, вычисляет статистику,
        генерирует отчет в желаемом формате и записывает его в файл.

        Шаги:
            1. Перебирает каждый путь, предоставленный в input_args.
            2. Определяет тип адреса (URL или FILE) и выбирает соответствующий парсер потока журналов.
            3. Потоковая обработка и фильтрация объектов журналов на основе критериев, указанных в input_args.
            4. Вычисляет статистику по отфильтрованным объектам журналов.
            5. Генерирует отчет, используя вычисленную статистику в указанном формате (Markdown или AsciiDoc).
            6. Записывает сгенерированное содержимое отчета в файл с соответствующим расширением.

        Возвращает:
            None

        Вызывает:
            HttpConectionError: При неудачном подключении к серверу с логами
            ReadFileError: Если возникает проблема при чтении в файл.
            IOError: Если возникает проблема при записи в файл.

        """

        for adress_type, adress_value in self.input_args.paths:
            match adress_type:
                case AdressTypes.URL:
                    log_stream = url_log_stream
                case AdressTypes.FILE:
                    log_stream = file_log_stream
                case _:
                    assert_never(adress_type)

            for log_object in log_stream(adress_value):
                if self._check_filter(log_object):
                    self.log_statistics_processor.calculate_statistics(log_object)

        log_statistics = self.log_statistics_processor.get_statistics()

        report_creator = BaseReportCreator(self.input_args, log_statistics)
        match self.input_args.format:
            case FormatTypes.MARKDOWN:
                generate_table_method = BaseReportCreator.generate_markdown_table
                header_symb = "####"

            case FormatTypes.ADOC:
                generate_table_method = BaseReportCreator.generate_adoc_table
                header_symb = "===="

            case _:
                assert_never(self.input_args.format)

        content_file = report_creator.create_report_content(
            generate_table_method, header_symb
        )

        self._write_to_file(content_file, f"report.{self.input_args.format}")

    def _check_filter(self, log_object: LogObject) -> bool:
        """
        Определяет, соответствует ли данный объект журнала критериям фильтрации, указанным в input_args.

        Критерии фильтрации:
            - Диапазон дат: Проверяет, находится ли local_time объекта журнала между from_date и to_date.
            - Фильтр по полю: Проверяет, соответствует ли указанное поле объекта журнала любому из значений фильтра.

        Аргументы:
            log_object (LogObject): Объект журнала, который необходимо оценить по фильтрам.

        Возвращает:
            bool: True, если объект журнала удовлетворяет всем условиям фильтрации, иначе False.

        Вызывает:
            AttributeError: Если указанное поле фильтра не существует в LogObject.
        """
        conditions = []

        if self.input_args.from_date:
            conditions.append(self.input_args.from_date <= log_object.local_time)

        if self.input_args.to_date:
            conditions.append(self.input_args.to_date >= log_object.local_time)

        if self.input_args.filter_field:
            filter_match = [
                filter_value == getattr(log_object, self.input_args.filter_field)
                for filter_value in self.input_args.filter_value
            ]
            conditions.append(any(filter_match))

        return all(conditions)

    def _write_to_file(self, content: str, filename: str) -> None:
        """
        Записывает предоставленное содержимое в файл с указанным именем.

        Аргументы:
            content (str): Содержимое, которое будет записано в файл.
            filename (str): Имя файла, в который будет записано содержимое.

        Возвращает:
            None

        Вызывает:
            IOError: Если файл не может быть открыт или записан.
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
        except IOError as e:
            raise IOError(f"Не удалось записать в файл {filename}.") from e
