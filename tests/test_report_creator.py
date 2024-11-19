import pytest
from src.log_statistics_processor import LogStatistics
from src.project_types import InputArgs,LogFields
from src.config import percentile_ratio
from src.report_creator import BaseReportCreator   

@pytest.fixture
def mock_input_args():
    """Фикстура для создания mock-объекта InputArgs."""
    return InputArgs(
        paths=[("path1", "/var/logs/access.log"), ("path2", "/var/logs/error.log")],
        from_date=None,
        to_date=None,
        format='md',
        filter_field=LogFields.METHOD.value,
        filter_value='GET'
    )

@pytest.fixture
def mock_log_stats():

    """Фикстура для создания mock-объекта LogStatistics."""
    return LogStatistics(
        logs_count=1000,
        average_response_size=500,
        percentile=800,
        status_code_frequency={200: 700, 404: 200, 500: 100},
        unique_users_number=150,
        resource_frequency={"resource1": 400, "resource2": 600},
    )

@pytest.fixture
def base_report_creator(mock_input_args, mock_log_stats):
    """Фикстура для инициализации BaseReportCreator."""
    creator = BaseReportCreator(mock_input_args, mock_log_stats)
     
    return creator

def test_generate_markdown_table(base_report_creator):
    headers = ["Header1", "Header2"]
    rows = [["Row1Col1", "Row1Col2"], ["Row2Col1", "Row2Col2"]]
    expected_table = (
        "| Header1 | Header2 |\n"
        "|:-------|:-------|\n"
        "| Row1Col1 | Row1Col2 |\n"
        "| Row2Col1 | Row2Col2 |"
    )
    result = base_report_creator.generate_markdown_table(headers, rows)
    assert result == expected_table

def test_generate_adoc_table(base_report_creator):
    headers = ["Header1", "Header2"]
    rows = [["Row1Col1", "Row1Col2"], ["Row2Col1", "Row2Col2"]]
    expected_table = (
        '[options="header"]\n|===\n'
        "| Header1 | Header2\n"
        "| Row1Col1 | Row1Col2\n"
        "| Row2Col1 | Row2Col2\n"
        "|==="
    )
    result = base_report_creator.generate_adoc_table(headers, rows)

    assert result == expected_table

def test_create_report_content(base_report_creator ):
    content = base_report_creator.create_report_content(base_report_creator.generate_markdown_table, "#")
 
    assert "Общая информация" in content
    assert "Запрашиваемые ресурсы" in content
    assert "Коды ответа" in content

def test_successful_unsuccessful_requests(base_report_creator):
    assert base_report_creator.successful_requests == 700
    assert base_report_creator.unsuccessful_requests == 300

def test_general_info_rows(base_report_creator):
    expected_general_info = [
        ["Файл(-ы)", "/var/logs/access.log, /var/logs/error.log"],
        ["Начальная дата", "-"],
        ["Конечная дата", "-"],
        ["Количество запросов", "1_000"],
        ["Средний размер ответа", "500b"],
        [f"{percentile_ratio * 100}p размера ответа", "800b"],
        ["Соотношение успешных запросов к общему количеству", "700 успешных / 1000 всего"],
        ["Количество уникальных посетителей", "150"],
    ]
    assert base_report_creator.general_info_rows == expected_general_info
