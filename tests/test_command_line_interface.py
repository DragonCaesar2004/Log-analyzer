import pytest
from unittest.mock import patch, MagicMock
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
    EmptyFilterValueError,
    DateOrderError,
    EmptyArgumentError,
    MoreOneArgumentError,
    DeployFilePatternError,
)
from src.project_types import InputArgs, AdressTypes
from src.config import LogFields
from datetime import datetime
from src.command_line_interface import (
    CommandLineInterface,
)  # Assuming the class is in cli.py


# Fixtures
@pytest.fixture
def cli_instance():
    return CommandLineInterface()


@pytest.fixture
def valid_args():
    return {
        "path": ["/path/to/logfile.log"],
        "from_date": ["2024-01-01T12:00:00"],
        "to_date": ["2024-01-02T12:00:00"],
        "format": ["json"],
        "filter_field": ["field_name"],
        "filter_value": ["value"],
    }


# Mock `glob.glob` for file path testing
@pytest.fixture
def mock_glob():
    with patch("glob.glob") as mock_glob:
        yield mock_glob


# Tests


def test_unknown_args(cli_instance):
    args = ["--unknown-arg"]
    with pytest.raises(UnknownArgumentsError):
        cli_instance._validate_unknown_args(args)


def test_missing_path(cli_instance):
    with pytest.raises(MissingPathError):
        cli_instance._validate_path(None)


def test_invalid_path(cli_instance):
    with patch("os.path.isfile", return_value=False):
        with pytest.raises(InvalidPathError):
            cli_instance._validate_path(["invalid/path"])


def test_valid_file_path(cli_instance):
    with patch("os.path.isfile", return_value=True):
        result = cli_instance._validate_path(["valid/path/to/file"])
        assert result == [(AdressTypes.FILE, "valid/path/to/file")]


def test_valid_url(cli_instance):
    valid_url = "http://example.com/file"
    assert cli_instance._is_url(valid_url)


def test_invalid_url(cli_instance):
    invalid_url = "ftp://example.com/file"
    assert not cli_instance._is_url(invalid_url)


def test_valid_datetime(cli_instance):
    date_str = ["2024-01-01T12:00:00"]
    result = cli_instance._validate_datetime_string(date_str)
    assert result == datetime(2024, 1, 1, 12, 0, 0)


def test_invalid_datetime_format(cli_instance):
    date_str = ["2024-01-01 12:00:00"]  # Missing 'T'
    with pytest.raises(InvalidDateFormatError):
        cli_instance._validate_datetime_string(date_str)


def test_date_order_error(cli_instance):
    start_date = datetime(2024, 1, 2, 12, 0, 0)
    end_date = datetime(2024, 1, 1, 12, 0, 0)
    with pytest.raises(DateOrderError):
        cli_instance._validate_date_order(start_date, end_date)


def test_valid_format(cli_instance):
    format_str = ["json"]
    result = cli_instance._validate_format_style(format_str)
    assert result == "json"


def test_invalid_format(cli_instance):
    format_str = ["xml"]  # Assuming 'xml' is not in `formats`
    with pytest.raises(InvalidFormatStyleError):
        cli_instance._validate_format_style(format_str)


def test_valid_filter_field(cli_instance):
    with patch("src.config.LogFields", new=["field_name"]):
        filter_field = ["field_name"]
        result = cli_instance._validate_filter_field(filter_field)
        assert result == "field_name"


def test_missing_filter_value(cli_instance):
    with pytest.raises(EmptyFilterValueError):
        cli_instance._validate_filter_value("field_name", None)


def test_empty_argument(cli_instance):
    args = MagicMock()
    args.path = []
    with pytest.raises(EmptyArgumentError):
        cli_instance._check_missing_params(args)


def test_one_argument(cli_instance):
    args = MagicMock()
    args.format = ["json", "xml"]  # Assuming `format` should only accept one value
    with pytest.raises(MoreOneArgumentError):
        cli_instance._check_one_argument(args)


def test_deploy_file_paths(cli_instance, mock_glob):
    mock_glob.return_value = ["/path/to/file1.log", "/path/to/file2.log"]
    paths = ["/path/*"]
    result = cli_instance._deploy_file_paths(paths)
    assert result == ["/path/to/file1.log", "/path/to/file2.log"]


def test_deploy_file_paths_no_files(cli_instance, mock_glob):
    mock_glob.return_value = []
    with pytest.raises(NoFilesFoundError):
        cli_instance._deploy_file_paths(["/path/*"])
