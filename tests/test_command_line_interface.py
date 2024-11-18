import pytest
import sys
from unittest import mock
from unittest.mock import patch

from src.user_interfaces.command_line_interface import CommandLineInterface
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
    DeployFilePatternError,
)
from src.project_types import InputArgs, FormatTypes

# Фикстура для CommandLineInterface
@pytest.fixture
def cli():
    cli_instance = CommandLineInterface()
    cli_instance.init()
    return cli_instance

# Фикстура для мока методов в CommandLineInterface
@pytest.fixture
def mock_validate_methods(mocker):
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_unknown_args')
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._check_missing_params')
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._check_one_argument')
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._deploy_file_paths', return_value=['/fake/path.log'])
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_path', return_value=['/fake/path.log'])
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_datetime_string', side_effect=lambda x: x[0] if x else None)
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_date_order')
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_format_style', return_value=FormatTypes.JSON)
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_filter_field', return_value='status')
    mocker.patch('src.user_interfaces.command_line_interface.CommandLineInterface._validate_filter_value', return_value='200')

def test_valid_arguments(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--from-date", "2023-01-01",
        "--to-date", "2023-12-31",
        "--format", "json",
        "--filter-field", "status",
        "--filter-value", "200"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    input_args = cli.get_init_data()

    assert input_args.paths == ['/fake/path.log']
    assert input_args.from_date == "2023-01-01"
    assert input_args.to_date == "2023-12-31"
    assert input_args.format == FormatTypes.JSON
    assert input_args.filter_field == 'status'
    assert input_args.filter_value == '200'

def test_missing_path(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "--from-date", "2023-01-01"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    with pytest.raises(MissingPathError):
        cli.get_init_data()

def test_unknown_arguments(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",

        "-p", "/fake/path.log",
        "--unknown-arg", "value"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки неизвестных аргументов
    cli._validate_unknown_args.side_effect = UnknownArgumentsError("Unknown argument provided.")

    with pytest.raises(UnknownArgumentsError):
        cli.get_init_data()

def test_invalid_date_format(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--from-date", "invalid-date"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки формата даты
    def side_effect_validate_datetime(x):
        if x[0] == "invalid-date":
            raise InvalidDateFormatError("Invalid date format.")

    cli._validate_datetime_string.side_effect = side_effect_validate_datetime

    with pytest.raises(InvalidDateFormatError):
        cli.get_init_data()

def test_invalid_format_style(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--format", "unknown_format"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки стиля формата
    cli._validate_format_style.side_effect = InvalidFormatStyleError("Unknown format style.")

    with pytest.raises(InvalidFormatStyleError):
        cli.get_init_data()

def test_missing_filter_field(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--filter-value", "200"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки отсутствия поля фильтрации
    def side_effect_validate_filter_field(x):
        if not x:
            raise MissingFilterFieldError("Filter field is missing.")

    cli._validate_filter_field.side_effect = side_effect_validate_filter_field

    with pytest.raises(MissingFilterFieldError):
        cli.get_init_data()

def test_empty_filter_value(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--filter-field", "status",
        "--filter-value", ""
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки пустого значения фильтра
    def side_effect_validate_filter_value(field, value):
        if not value:
            raise EmptyFilterValueError("Filter value is empty.")

    cli._validate_filter_value.side_effect = side_effect_validate_filter_value

    with pytest.raises(EmptyFilterValueError):
        cli.get_init_data()

def test_date_order(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--from-date", "2023-12-31",
        "--to-date", "2023-01-01"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки порядка дат
    def side_effect_validate_date_order(from_date, to_date):
        if from_date > to_date:
            raise DateOrderError("From date is after To date.")

    cli._validate_date_order.side_effect = side_effect_validate_date_order

    with pytest.raises(DateOrderError):
        cli.get_init_data()

def test_unknown_exception(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для неизвестной ошибки
    cli._validate_unknown_args.side_effect = Exception("Unknown error.")

    with pytest.raises(Exception) as exc_info:
        cli.get_init_data()
    assert str(exc_info.value) == "Unknown error."



# Тест на отсутствие аргумента --path
def test_missing_path(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "--from-date", "2023-01-01T00:00:00"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    with pytest.raises(MissingPathError):
        cli.get_init_data()


# Тест на наличие неизвестных аргументов
def test_unknown_arguments(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--unknown-arg", "value"
    ]
    
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки неизвестных аргументов
    cli._validate_unknown_args.side_effect = UnknownArgumentsError(["--unknown-arg"])

    with pytest.raises(UnknownArgumentsError) as exc_info:
        cli.get_init_data()
    
    assert exc_info.value.args[0] == ["--unknown-arg"]


# Тест на неверный формат даты
def test_invalid_date_format(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--from-date", "invalid-date"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки формата даты
    def side_effect_validate_datetime(x):
        if x[0] == "invalid-date":
            raise InvalidDateFormatError("invalid-date")
        return x[0]

    cli._validate_datetime_string.side_effect = side_effect_validate_datetime

    with pytest.raises(InvalidDateFormatError) as exc_info:
        cli.get_init_data()
    
    assert exc_info.value.args[0] == "invalid-date"


# Тест на некорректное значение даты
def test_invalid_date_value(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--from-date", "2023-02-30T00:00:00"  # 30 февраля не существует
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки значения даты
    def side_effect_validate_datetime(x):
        if x[0] == "2023-02-30T00:00:00":
            raise InvalidDateValueError()
        return x[0]

    cli._validate_datetime_string.side_effect = side_effect_validate_datetime

    with pytest.raises(InvalidDateValueError):
        cli.get_init_data()


# Тест на неизвестный формат стиля
def test_invalid_format_style(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--format", "unknown_format"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки стиля формата
    cli._validate_format_style.side_effect = InvalidFormatStyleError([fmt.value for fmt in FormatTypes])

    with pytest.raises(InvalidFormatStyleError) as exc_info:
        cli.get_init_data()
    
    assert exc_info.value.args[0] == [fmt.value for fmt in FormatTypes]


# Тест на отсутствие поля фильтрации при наличии значения фильтра
def test_missing_filter_field(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--filter-value", "200"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки отсутствия поля фильтрации
    cli._validate_filter_field.side_effect = MissingFilterFieldError()

    with pytest.raises(MissingFilterFieldError):
        cli.get_init_data()


# Тест на пустое значение фильтра
def test_empty_filter_value(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--filter-field", "status",
        "--filter-value", ""
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки пустого значения фильтра
    def side_effect_validate_filter_value(field, value):
        if not value or value[0] == "":
            raise EmptyFilterValueError()
        return value

    cli._validate_filter_value.side_effect = side_effect_validate_filter_value

    with pytest.raises(EmptyFilterValueError):
        cli.get_init_data()


# Тест на некорректный порядок дат
def test_date_order(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log",
        "--from-date", "2023-12-31T23:59:59",
        "--to-date", "2023-01-01T00:00:00"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для проверки порядка дат
    def side_effect_validate_date_order(from_date, to_date):
        if from_date > to_date:
            raise DateOrderError("From date is after To date.")

    cli._validate_date_order.side_effect = side_effect_validate_date_order

    with pytest.raises(DateOrderError) as exc_info:

        cli.get_init_data()
    
    assert exc_info.value.args[0] == "From date is after To date."


# Тест на неизвестную ошибку
def test_unknown_exception(cli, mock_validate_methods, monkeypatch):
    test_args = [
        "prog",
        "-p", "/fake/path.log"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Настраиваем мок для неизвестной ошибки
    cli._validate_unknown_args.side_effect = Exception("Unknown error.")

    with pytest.raises(Exception) as exc_info:
        cli.get_init_data()
    
    assert str(exc_info.value) == "Unknown error."


# Дополнительные тесты для новых методов

# Тест метода _is_url
def test_is_url(cli):
    assert cli._is_url("http://example.com") is True
    assert cli._is_url("https://example.com") is True
    assert cli._is_url("ftp://example.com") is False
    assert cli._is_url("/local/path.log") is False


# Тест метода _is_file
@patch('os.path.isfile')
def test_is_file(mock_isfile, cli):
    mock_isfile.side_effect = lambda path: path == "/existing/file.log"

    assert cli._is_file("/existing/file.log") is True
    assert cli._is_file("/nonexistent/file.log") is False


# Тест метода _deploy_file_paths с файлами и URL
@patch('glob.glob')
def test_deploy_file_paths_with_files_and_urls(mock_glob, cli):
    paths = [
        "http://example.com/log",
        "/local/path1.log",
        "/local/path2.log"
    ]

    # Настраиваем функции проверки URL и файла
    with patch.object(cli, '_is_url', side_effect=lambda x: x.startswith("http")):
        with patch.object(cli, '_is_file', side_effect=lambda x: x.startswith("/local")):
            # Настраиваем glob
            mock_glob.side_effect = [
                ["/local/path1.log"],
                ["/local/path2.log"]
            ]

            result = cli._deploy_file_paths(paths)
            expected = ["/local/path1.log", "/local/path2.log", "http://example.com/log"]
            assert result == expected


# Тест метода _deploy_file_paths с отсутствующими файлами
@patch('glob.glob')
def test_deploy_file_paths_no_files_found(mock_glob, cli):
    paths = [
        "/nonexistent/path.log"
    ]

    # Настраиваем функции проверки URL и файла
    with patch.object(cli, '_is_url', return_value=False):
        with patch.object(cli, '_is_file', return_value=False):
            # Настраиваем glob
            mock_glob.return_value = []

            with pytest.raises(NoFilesFoundError) as exc_info:
                cli._deploy_file_paths(paths)
            
            assert exc_info.value.args[0] == "/nonexistent/path.log"


# Тест метода _validate_path с валидными и невалидными путями
@patch('os.path.isfile')
def test_validate_path(mock_isfile, cli):
    paths = [
        "http://example.com/log",
        "/local/path1.log",
        "/invalid/path.log"
    ]

    # Настраиваем _is_url и _is_file
    with patch.object(cli, '_is_url', side_effect=lambda x: x.startswith("http")):
        with patch.object(cli, '_is_file', side_effect=lambda x: x == "/local/path1.log"):
            with patch('glob.glob', return_value=["/local/path1.log"]):
                with pytest.raises(InvalidPathError) as exc_info:
                    cli._validate_path(paths)
                
                assert exc_info.value.args[0] == "/invalid/path.log"

            # Если все пути валидны
            with patch('glob.glob', return_value=["/local/path1.log"]):
                valid_paths = cli._validate_path(["http://example.com/log", "/local/path1.log"])
                expected = [
                    (AdressTypes.URL, "http://example.com/log"),
                    (AdressTypes.FILE, "/local/path1.log")
                ]
                assert valid_paths == expected


# Тест метода _validate_datetime_string с валидной датой
def test_validate_datetime_string_valid(cli):
    date_list = ["2023-01-01T12:00:00"]
    result = cli._validate_datetime_string(date_list)
    assert isinstance(result, datetime)
    assert result == datetime(2023, 1, 1, 12, 0, 0)


# Тест метода _validate_datetime_string с невалидным форматом

def test_validate_datetime_string_invalid_format(cli):
    date_list = ["2023/01/01 12:00:00"]
    with pytest.raises(InvalidDateFormatError) as exc_info:
        cli._validate_datetime_string(date_list)
    
    assert exc_info.value.args[0] == "2023/01/01 12:00:00"


# Тест метода _validate_datetime_string с невалидным значением даты
def test_validate_datetime_string_invalid_value(cli):
    date_list = ["2023-02-30T12:00:00"]  # Неверная дата
    with pytest.raises(InvalidDateValueError):
        cli._validate_datetime_string(date_list)


# Тест метода _validate_format_style с валидным форматом
def test_validate_format_style_valid(cli):
    format_input = ["json"]
    result = cli._validate_format_style(format_input)
    assert result == FormatTypes.JSON


# Тест метода _validate_format_style с отсутствующим форматом (должен вернуть значение по умолчанию)
def test_validate_format_style_default(cli):
    result = cli._validate_format_style(None)
    assert result == FormatTypes.MARKDOWN.value


# Тест метода _validate_format_style с неизвестным форматом
def test_validate_format_style_invalid(cli):
    format_input = ["unknown_format"]
    with pytest.raises(InvalidFormatStyleError) as exc_info:
        cli._validate_format_style(format_input)
    
    assert exc_info.value.args[0] == [fmt.value for fmt in FormatTypes]


# Тест метода _validate_filter_field с валидным полем
def test_validate_filter_field_valid(cli):
    filter_field = ["status"]
    result = cli._validate_filter_field(filter_field)
    assert result == LogFields.STATUS


# Тест метода _validate_filter_field с невалидным полем
def test_validate_filter_field_invalid(cli):
    filter_field = ["unknown_field"]
    with pytest.raises(InvalidFilterFieldError) as exc_info:
        cli._validate_filter_field(filter_field)
    
    assert exc_info.value.args[0] == list(LogFields)


# Тест метода _validate_filter_value с валидными значениями
def test_validate_filter_value_valid(cli):
    filter_field = LogFields.STATUS
    filter_value = ["200"]
    result = cli._validate_filter_value(filter_field, filter_value)
    assert result == ["200"]


# Тест метода _validate_filter_value без значения фильтра
def test_validate_filter_value_none(cli):
    filter_field = LogFields.STATUS
    filter_value = None
    with pytest.raises(EmptyFilterValueError):
        cli._validate_filter_value(filter_field, filter_value)


# Тест метода _validate_filter_value без поля фильтра при наличии значения
def test_validate_filter_value_missing_field(cli):
    filter_field = None
    filter_value = ["200"]
    with pytest.raises(MissingFilterFieldError):
        cli._validate_filter_value(filter_field, filter_value)


# Тест метода _validate_filter_value с отсутствием поля и значения
def test_validate_filter_value_none_both(cli):
    filter_field = None
    filter_value = None
    result = cli._validate_filter_value(filter_field, filter_value)
    assert result is None
