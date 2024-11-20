import pytest
from datetime import datetime
import argparse
from src.user_interfaces.command_line_interface import CommandLineInterface
from src.project_types import AdressTypes, FormatTypes, LogFields
from src.custom_exceptions import (
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
    NoFilesFoundError,
     
)

@pytest.fixture(scope = 'session')
def cli():
    """Фикстура для создания экземпляра CommandLineInterface."""
    return CommandLineInterface()


def test_validate_unknown_args(cli):
    with pytest.raises(UnknownArgumentsError):
        cli._validate_unknown_args(["--unknown"])


def test_deploy_correct_file_paths(cli, mocker):
    # Успешное выполнение
    mocker.patch("src.user_interfaces.command_line_interface.glob", return_value=["file1.log", "file2.log"])
    paths = cli._deploy_file_paths(["file*.log"])
    assert paths == ["file1.log", "file2.log"]

def test_deploy_wrong_file_paths(cli, mocker):
    # Ошибка: нет файлов по шаблону
    mocker.patch("src.user_interfaces.command_line_interface.glob", return_value=[])
    with pytest.raises(NoFilesFoundError) :
        cli._deploy_file_paths(["not_exist*.log"])
 

def test_validate_path(cli, mocker):
    mocker.patch("os.path.isfile", return_value=True)
    paths = cli._validate_path(["file.log"])
    assert paths == [(AdressTypes.FILE, "file.log")]

    mocker.patch("os.path.isfile", return_value=False)
    with pytest.raises(InvalidPathError):
        cli._validate_path(["invalid_path"])


def test_validate_datetime_string(cli):
    valid_date = "2023-11-20T10:30:00"
    result = cli._validate_datetime_string([valid_date])
    assert result == datetime.strptime(valid_date, "%Y-%m-%dT%H:%M:%S")

    with pytest.raises(InvalidDateFormatError):
        cli._validate_datetime_string(["2023-11-20"])

    with pytest.raises(InvalidDateValueError):
        cli._validate_datetime_string(["2023-99-20T10:30:00"])


def test_validate_format_style(cli):
    assert cli._validate_format_style(["md"]) == FormatTypes.MARKDOWN
    assert cli._validate_format_style(["adoc"]) == FormatTypes.ADOC

    with pytest.raises(InvalidFormatStyleError):
        cli._validate_format_style(["INVALID_FORMAT"])


def test_validate_filter_field(cli):
    assert cli._validate_filter_field(["ip_addr"]) == LogFields.IP_ADDR
    assert cli._validate_filter_field(["user_name"]) == LogFields.USER_NAME
    assert cli._validate_filter_field(["local_time"]) == LogFields.LOCAL_TIME
    assert cli._validate_filter_field(["method"]) == LogFields.METHOD
    assert cli._validate_filter_field(["resource"]) == LogFields.RESOURCE
    assert cli._validate_filter_field(["http_version"]) == LogFields.HTTP_VERSION
    assert cli._validate_filter_field(["status_code"]) == LogFields.STATUS_CODE
    assert cli._validate_filter_field(["body_bytes_sent"]) == LogFields.BODY_BYTES_SENT
    assert cli._validate_filter_field(["http_referer"]) == LogFields.HTTP_REFERER
    assert cli._validate_filter_field(["http_user_agent"]) == LogFields.HTTP_USER_AGENT

    with pytest.raises(InvalidFilterFieldError):
        cli._validate_filter_field(["unknown_field"])


def test_validate_filter_value(cli):
    assert cli._validate_filter_value(LogFields.LOCAL_TIME, ['17/May/2015:08:05:09','22/May/2015:08:05:09']) == ['17/May/2015:08:05:09','22/May/2015:08:05:09']

    with pytest.raises(EmptyFilterValueError):
        cli._validate_filter_value(LogFields.LOCAL_TIME, None)

    with pytest.raises(MissingFilterFieldError):
        cli._validate_filter_value(None, ["17/May/2015:08:05:09"])


def test_validate_date_order(cli):
    start_date = datetime(2023, 11, 19, 10, 30, 0)
    end_date = datetime(2023, 11, 20, 10, 30, 0)
    assert cli._validate_date_order(start_date=start_date, end_date=end_date) is None

    with pytest.raises(DateOrderError):
        cli._validate_date_order(start_date=end_date, end_date = start_date)


def test_check_missing_params(cli):
    args = argparse.Namespace(path=["file.log"], from_date=None) # Если не указывали флаг
    assert cli._check_missing_params(args) is None

    args = argparse.Namespace(path=["file.log"], from_date=[]) # Если указали флаг
    with pytest.raises(EmptyArgumentError):
        cli._check_missing_params(args)


def test_check_one_argument(cli):
    args = argparse.Namespace(path=["file.log"], format=["md"])
    assert cli._check_one_argument(args) is None 

    args = argparse.Namespace(path=["file.log"], format=["md", "adoc"])
    with pytest.raises(MoreOneArgumentError):
        cli._check_one_argument(args)

def test_is_file(cli, mocker):
    mocker.patch("os.path.isfile", return_value=True)
    assert cli._is_file("file.log") is True

    mocker.patch("os.path.isfile", return_value=False)
    assert cli._is_file("invalid_file.log") is False


def test_is_url(cli):
    assert cli._is_url("http://example.com") is True
    assert cli._is_url("https://example.com") is True
    assert cli._is_url("ftp://example.com") is False
    assert cli._is_url("file.log") is False


def test_get_user_data(cli, mocker):
    """Проверяем корректную работу get_user_data"""
    mock_args = argparse.Namespace(
        path=["file.log"],
        from_date=[datetime.strptime("2023-11-20T10:30:00", "%Y-%m-%dT%H:%M:%S")],
        to_date=None,
        format=["md"],
        filter_field=["method"],
        filter_value=['GET'],
    )
    mocker.patch("argparse.ArgumentParser.parse_known_args", return_value=(mock_args, []))
    mocker.patch.object(cli, "_validate_args", return_value=mock_args)
    
    result = cli.get_user_data()
    assert result.path == mock_args.path
    print(result.from_date[0])
    print(datetime.strptime("2023-11-20T10:30:00", "%Y-%m-%dT%H:%M:%S"))
    assert result.from_date[0] == datetime.strptime("2023-11-20T10:30:00", "%Y-%m-%dT%H:%M:%S")


def test_validate_args(cli, mocker):
    """Проверяем обработку всех аргументов в `_validate_args`."""
    args = argparse.Namespace(
        path=["http://example.com"],
        from_date=["2023-11-20T10:30:00"],
        to_date=["2023-11-21T10:30:00"],
        format=["md"],
        filter_field=["method"],
        filter_value=["GET"],
    )
    mocker.patch.object(cli, "_validate_unknown_args")
    mocker.patch.object(cli, "_check_missing_params")
    mocker.patch.object(cli, "_check_one_argument")
    mocker.patch.object(cli, "_deploy_file_paths", return_value=["http://example.com"])
    mocker.patch.object(cli, "_validate_path", return_value=[(AdressTypes.URL, "http://example.com")])
    mocker.patch.object(cli, "_validate_datetime_string", side_effect=[
        datetime(2023, 11, 20, 10, 30, 0), datetime(2023, 11, 21, 10, 30, 0)
    ])
    mocker.patch.object(cli, "_validate_format_style", return_value=FormatTypes.MARKDOWN)
    mocker.patch.object(cli, "_validate_filter_field", return_value=LogFields.METHOD)
    mocker.patch.object(cli, "_validate_filter_value", return_value=["GET"])

    result = cli._validate_args(args, [])
    assert result.paths == [(AdressTypes.URL, "http://example.com")]
    assert result.from_date == datetime(2023, 11, 20, 10, 30, 0)
    assert result.to_date == datetime(2023, 11, 21, 10, 30, 0)
    assert result.format == FormatTypes.MARKDOWN
    assert result.filter_field == LogFields.METHOD
    assert result.filter_value == ["GET"]


 

 