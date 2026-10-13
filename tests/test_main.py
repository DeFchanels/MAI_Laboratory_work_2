import json
import sys

import pytest

from globals import report
from streamstats.__main__ import main


@pytest.fixture(autouse=True) # Перед каждым тестом очищаем глобальную переменную report
def reset_report():
    report.clear()
    report.update({
        "total_events": 0,
        "total_valid_events": 0,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
        },
        "top_errors_sources": {
        },
        "first_timestamp": None,
        "last_timestamp": None,
        "invalid_events_skipped": 0
    })


def test_main_analyze_command(tmp_path, monkeypatch):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        '{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}\n{"timestamp": "2026-10-09T08:00:00Z", "level": "ERROR", "source": "reg", "message": ""}\n{"timestamp": "2026-10-09T15:00:00Z", "level": "WARNING", "source": "web", "message": ""}'
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 3,
        "total_valid_events": 3,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 1,
            "ERROR": 1,
            "CRITICAL": 0
        },
        "sources_counters": {
            "auth": 1,
            "reg": 1,
            "web": 1
        },
        "top_errors_sources": {
            "reg": 1,
            "auth": 0,
            "web": 0
        },
        "first_timestamp": "2026-10-09T08:00:00Z",
        "last_timestamp": "2026-10-09T15:00:00Z",
        "invalid_events_skipped": 0
    }
    assert result == expected_result


def test_empty_file(tmp_path, monkeypatch):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл пустой строкой
        ""
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 0,
        "total_valid_events": 0,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
        },
        "top_errors_sources": {
        },
        "first_timestamp": None,
        "last_timestamp": None,
        "invalid_events_skipped": 0
    }
    assert result == expected_result


def test_main_unicode(tmp_path, monkeypatch):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        '{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "Аутентификация 👾", "message": "Пользователь зашел в аккаунт 👍"}'
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 1,
        "total_valid_events": 1,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
            "Аутентификация 👾": 1
        },
        "top_errors_sources": {
            "Аутентификация 👾": 0
        },
        "first_timestamp": "2026-10-09T12:00:00Z",
        "last_timestamp": "2026-10-09T12:00:00Z",
        "invalid_events_skipped": 0
    }
    assert result == expected_result


def test_main_csv(tmp_path, monkeypatch):
    input_file = tmp_path / "input.csv" # Создаем временный input csv файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        "timestamp,level,source,message\n"
        "2026-10-09T10:00:00Z,WARNING,auth,warning_message\n"
        "2026-10-09T10:50:00Z,INFO,reg,registered\n"
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "csv", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 2,
        "total_valid_events": 2,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 1,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
            "auth": 1,
            "reg": 1
        },
        "top_errors_sources": {
            "auth": 0,
            "reg": 0
        },
        "first_timestamp": "2026-10-09T10:00:00Z",
        "last_timestamp": "2026-10-09T10:50:00Z",
        "invalid_events_skipped": 0
    }
    assert result == expected_result


def test_main_broken_line_skipped(tmp_path, monkeypatch, caplog):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        '{"timestamp": "2026-10-09T10:00:00Z"broken_line\n{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}'
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--skip-invalid", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 2,
        "total_valid_events": 1,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
            "auth": 1
        },
        "top_errors_sources": {
            "auth": 0
        },
        "first_timestamp": "2026-10-09T12:00:00Z",
        "last_timestamp": "2026-10-09T12:00:00Z",
        "invalid_events_skipped": 1
    }
    assert result == expected_result
    assert "WARNING" in caplog.text
    assert "Error occurred while reading a file line:" in caplog.text


def test_main_broken_line_without_skip(tmp_path, capsys, monkeypatch):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        '{"timestamp": "2026-10-09T10:00:00Z"broken_line\n{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}'
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    with pytest.raises(SystemExit) as exit_info:
        main()
    captured = capsys.readouterr()  # Считываем вывод
    assert exit_info.value.code == 2
    assert 'Error occurred while reading a file line:' in captured.err.strip()


def test_main_invalid_timestamp(tmp_path, capsys, monkeypatch, caplog):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        '{"timestamp": "2026-:00Z", "level": "INFO", "source": "auth", "message": ""}\n{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}'
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--skip-invalid", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 2,
        "total_valid_events": 1,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
            "auth": 1
        },
        "top_errors_sources": {
            "auth": 0
        },
        "first_timestamp": "2026-10-09T12:00:00Z",
        "last_timestamp": "2026-10-09T12:00:00Z",
        "invalid_events_skipped": 1
    }
    assert result == expected_result
    assert "WARNING" in caplog.text
    assert 'Skipped invalid event at' in caplog.text and 'Invalid timestamp' in caplog.text



def test_main_two_different_errors(tmp_path, capsys, monkeypatch, caplog):
    input_file = tmp_path / "input.jsonl" # Создаем временный input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file.write_text( # Заполняем временный файл
        '{"timestamp": "2026-:00Z", "level": "INFO", "source": "auth", "message": ""}\n{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "", "message": ""}'
    )
    cli_args = ["streamstats", "analyze", str(input_file), "--format", "jsonl", "--skip-invalid", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 2,
        "total_valid_events": 0,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {
        },
        "top_errors_sources": {
        },
        "first_timestamp": None,
        "last_timestamp": None,
        "invalid_events_skipped": 2
    }
    assert result == expected_result
    assert "WARNING" in caplog.text
    assert 'Skipped invalid event at' in caplog.text and 'Invalid timestamp' in caplog.text and 'Source is empty' in caplog.text



def test_main_two_files(tmp_path, capsys, monkeypatch):
    input_file_1 = tmp_path / "input_1.jsonl" # Создаем временный первый input jsonl файл
    input_file_2 = tmp_path / "input_2.jsonl"  # Создаем временный второй input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file_1.write_text( # Заполняем временный файл 1
        '{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}\n{"timestamp": "2026-10-09T13:00:00Z", "level": "WARNING", "source": "reg", "message": ""}'
    )
    input_file_2.write_text( # Заполняем временный файл 1
        '{"timestamp": "2026-10-09T10:00:00Z", "level": "ERROR", "source": "auth", "message": "error"}\n{"timestamp": "2026-10-09T15:00:00Z", "level": "CRITICAL", "source": "reg", "message": "critical error"}'
    )
    cli_args = ["streamstats", "analyze", str(input_file_1), str(input_file_2), "--format", "jsonl", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 4,
        "total_valid_events": 4,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 1,
            "ERROR": 1,
            "CRITICAL": 1
        },
        "sources_counters": {
            "auth": 2,
            "reg": 2
        },
        "top_errors_sources": {
            "auth": 1,
            "reg": 1
        },
        "first_timestamp": "2026-10-09T10:00:00Z",
        "last_timestamp": "2026-10-09T15:00:00Z",
        "invalid_events_skipped": 0
    }

    assert result == expected_result


def test_main_two_files_one_is_invalid_with_skip(tmp_path, capsys, monkeypatch, caplog):
    input_file_1 = tmp_path / "input_1.jsonl" # Создаем временный первый input jsonl файл
    input_file_2 = tmp_path / "input_2.jsonl"  # Создаем временный второй input jsonl файл
    output_file = tmp_path / "output.json" # Создаем временный output json файл
    input_file_1.write_text( # Заполняем временный файл 1
        '{"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}\n{"timestamp": "2026", "level": "WARNING", "source": "reg", "message": ""}'
    )
    input_file_2.write_text( # Заполняем временный файл 1
        '{"timestamp": "2026-10-09T10:00:00Z", "level": "ERROR", "source": "auth", "message": "error"}\n{"timestamp": "2026-10-09T15:00:00Z", "level": "CRITICAL", "source": "reg", "message": "critical error"}'
    )
    cli_args = ["streamstats", "analyze", str(input_file_1), str(input_file_2), "--format", "jsonl", "--skip-invalid", "--output", str(output_file)]
    monkeypatch.setattr(sys, "argv", cli_args)
    main()
    with open(output_file, "r") as f:
        result = json.load(f)
    expected_result = {
        "total_events": 4,
        "total_valid_events": 3,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 1,
            "CRITICAL": 1
        },
        "sources_counters": {
            "auth": 2,
            "reg": 1
        },
        "top_errors_sources": {
            "auth": 1,
            "reg": 1
        },
        "first_timestamp": "2026-10-09T10:00:00Z",
        "last_timestamp": "2026-10-09T15:00:00Z",
        "invalid_events_skipped": 1
    }

    assert result == expected_result
    assert "WARNING" in caplog.text
    assert 'Skipped invalid event at' in caplog.text and 'Invalid timestamp' in caplog.text