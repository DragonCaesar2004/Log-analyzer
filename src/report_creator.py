from src.log_statistics_processor import LogStatistics
from src.project_types import InputArgs
from src.config import percentile_ratio


class BaseReportCreator():

    def __init__(self, input_args: InputArgs, log_stats: LogStatistics)->None:
        self.general_info_headers = ["Метрика", "Значение"]

        # Извлечение адресов из входных аргументов
        self.paths = [address_value for _, address_value in input_args.paths]

        # Расчет успешных и неуспешных запросов
        self.successful_requests = sum(
            count for status, count in log_stats.status_code_frequency.items() if 200 <= status < 300
        )
        self.unsuccessful_requests = sum(
            count for status, count in log_stats.status_code_frequency.items() if not (200 <= status < 300)
        )

        # Подготовка строк для таблицы общей информации
        self.general_info_rows = [
            ["Файл(-ы)", ", ".join(self.paths)],
            [
                "Начальная дата",
                (
                    input_args.from_date.strftime("%d/%b/%Y:%H:%M:%S")
                    if input_args.from_date
                    else "-"
                ),
            ],
            [
                "Конечная дата",
                (
                    input_args.to_date.strftime("%d/%b/%Y:%H:%M:%S")
                    if input_args.to_date
                    else "-"
                ),
            ],
            ["Количество запросов", f"{log_stats.logs_count:,}".replace(",", "_")],
            ["Средний размер ответа", f"{str(log_stats.average_response_size)+'b' if log_stats.average_response_size>=0 else '-'}"],
            [f"{percentile_ratio*100}p размера ответа", f"{str(log_stats.percentile) +'b' if log_stats.percentile>=0 else '-' }"],
            [
                "Соотношение успешных запросов к общему количеству",
                f"{self.successful_requests} успешных / {log_stats.logs_count} всего",
            ],
            [
                "Количество уникальных посетителей",
                f"{log_stats.unique_users_number:,}".replace(",", "_"),
            ],
        ]
        self.resource_headers = ["Ресурс", "Количество"]
        self.resource_rows = [
            [resource, f"{count:,}".replace(",", "_")]
            for resource, count in log_stats.resource_frequency.items()
        ]
        self.status_headers = ["Код", "Количество"]
        self.status_rows = [
            [str(status_code), f"{count:,}".replace(",", "_")]
            for status_code, count in log_stats.status_code_frequency.items()
        ]

    def create_report(self, generate_table_method, header_symb: str)->str:
        content = f"{header_symb} Общая информация\n\n"
        # Добавление таблицы общей информации
        content += generate_table_method(
            self.general_info_headers, self.general_info_rows
        )
        content += f"\n\n{header_symb}  Запрашиваемые ресурсы\n\n"
        content += generate_table_method(self.resource_headers, self.resource_rows)
        content += f"\n\n{header_symb}  Коды ответа\n\n"
        content += generate_table_method(self.status_headers, self.status_rows)
        return content

    @staticmethod
    def generate_markdown_table(headers: list[str], rows: list[list[str]]) -> str:
        # Форматирование заголовков таблицы
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = (
            "|" + "|".join([":" + "-" * (len(header)) for header in headers]) + "|"
        )

        # Форматирование строк таблицы
        data_rows = ["| " + " | ".join(row) + " |" for row in rows]

        # Объединение всех частей

        table = "\n".join([header_row, separator_row] + data_rows)
        return table

    @staticmethod
    def generate_adoc_table(headers: list[str], rows: list[list[str]]) -> str:
        """
        Генерация таблицы в формате Asciidoc.

        :param headers: Список заголовков столбцов.
        :param rows: Список строк таблицы, каждая строка — список значений ячеек.
        :return: Строка с таблицей в формате Asciidoc.
        """
        # Начало таблицы с опцией header
        table = '[options="header"]\n|===\n'
        # Добавление заголовков
        table += "| " + " | ".join(headers) + "\n"
        # Добавление строк таблицы
        for row in rows:
            table += "| " + " | ".join(row) + "\n"
        # Закрытие таблицы
        table += "|==="
        return table


 