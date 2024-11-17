from typing import assert_never

from src.project_types import InputArgs, AdressTypes, FormatTypes
from src.parsers.url_parser import url_log_stream
from src.parsers.file_parser import file_log_stream
from src.log_object import LogObject
from src.log_statistics_processor import LogStatisticsProcessor
from src.report_creator import BaseReportCreator


class Manager:

    def __init__(self, input_args: InputArgs):
        self.input_args = input_args
        self.log_statistics_processor = LogStatisticsProcessor()

    def create_report(self) -> None:
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
            case FormatTypes.MARKDOWN.value:
                generate_table_method = BaseReportCreator.generate_markdown_table
                header_symb = "####"

            case FormatTypes.ADOC.value:
                generate_table_method = BaseReportCreator.generate_adoc_table
                header_symb = "===="

            case _:
                assert_never(self.input_args.format)

        content_file = report_creator.create_report(generate_table_method, header_symb)

        self._write_to_file(content_file, f"report.{self.input_args.format}")

    def _check_filter(self, log_object: LogObject) -> bool:
        conditions = []

        if self.input_args.from_date:
            conditions.append(self.input_args.from_date <= log_object.local_time)

        if self.input_args.to_date:
            conditions.append(self.input_args.to_date >= log_object.local_time)

        if self.input_args.filter_field:
            filter_match = [
                filter_value == getattr(log_object, self.input_args.filter_field.value)
                for filter_value in self.input_args.filter_value
            ]
            conditions.append(any(filter_match))

        return all(conditions)

    def _write_to_file(self, content: str, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
