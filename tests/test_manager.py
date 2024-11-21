import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
from src.project_types import InputArgs, AdressTypes, FormatTypes
from src.config import LogFields
from src.manager import Manager


@pytest.fixture
def input_args():
    return InputArgs(
        paths=[
            (AdressTypes.URL, "http://example.com/logs"),
            (AdressTypes.FILE, "/path/to/logfile.log"),
        ],
        from_date=datetime(2023, 1, 1, 11, 11, 11),
        to_date=datetime(2023, 12, 31, 11, 11, 11),
        filter_field=LogFields.STATUS_CODE,
        filter_value=[200, 404],
        format=FormatTypes.MARKDOWN,
    )


@pytest.fixture
def manager_instance(input_args):
    manager = Manager(input_args)
    return manager


@patch("builtins.open", new_callable=mock_open)
def test_write_to_file_success(mock_file, manager_instance):
    content = "Пример отчета"
    filename = "report.md"

    manager_instance._write_to_file(content, filename)

    mock_file.assert_called_once_with(filename, "w", encoding="utf-8")
    mock_file().write.assert_called_once_with(content)
