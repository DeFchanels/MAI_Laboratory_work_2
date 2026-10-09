import pytest
from streamstats.parsers import parse_file
from streamstats.errors import IncorrectEventError, CLIConfigureError


def test_parse_csv(tmp_path): # Парсинг файла csv
    csv_file = tmp_path / "input.csv"
    csv_file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-09T10:00:00Z,WARNING,auth,warning_message\n"
        "2026-10-09T10:50:00Z,INFO,reg,registered\n"
    )

    events = list(parse_file(str(csv_file), "csv", False))
    event_1, line_num_1 = events[0]
    event_2, line_num_2 = events[1]
    assert len(events) == 2
    assert event_1["source"] == "auth"
    assert event_1["level"] == "WARNING"
    assert event_1["timestamp"] == "2026-10-09T10:00:00Z"
    assert event_1["message"] == "warning_message"
    assert event_2["source"] == "reg"
    assert event_2["level"] == "INFO"
    assert event_2["timestamp"] == "2026-10-09T10:50:00Z"
    assert event_2["message"] == "registered"


def test_parse_jsonl(tmp_path): # Парсинг файла jsonl
    file = tmp_path / "data.jsonl"
    file.write_text(
        '{"timestamp": "2026-10-09T10:00:00Z", "level": "WARNING", "source": "auth", "message": "warning_message"}\n {"timestamp": "2026-10-09T10:50:00Z", "level": "INFO", "source": "reg", "message": "registered"}\n'
    )

    events = list(parse_file(str(file), "jsonl", False))
    event_1, line_num_1 = events[0]
    event_2, line_num_2 = events[1]
    assert len(events) == 2
    assert event_1["source"] == "auth"
    assert event_1["level"] == "WARNING"
    assert event_1["timestamp"] == "2026-10-09T10:00:00Z"
    assert event_1["message"] == "warning_message"
    assert event_2["source"] == "reg"
    assert event_2["level"] == "INFO"
    assert event_2["timestamp"] == "2026-10-09T10:50:00Z"
    assert event_2["message"] == "registered"


def test_parse_file_not_found(): # Введенный файл не найден
    with pytest.raises(CLIConfigureError):
        events = list(parse_file("non_existent_file.csv", "csv", False))


def test_parse_broken_jsonl_file(tmp_path): # Во время чтения jsonl файла встретилась поломанная строка (флаг skip-invalid = False)
    file = tmp_path / "input.jsonl"
    file.write_text('{"timestamp": "2026-10-09T10:00:00Z"}\n{broken_line\n')
    with pytest.raises(IncorrectEventError):
        list(parse_file(str(file), "jsonl", False))


def test_parse_file_wrong_extension(tmp_path): # Тип файла не совпадает с введенным
    wrong_file = tmp_path / "input.txt"
    wrong_file.write_text("timestamp,level,source,message\n"
        "2026-10-09T10:00:00Z,WARNING,auth,warning_message\n"
        "2026-10-09T10:50:00Z,INFO,reg,registered\n")

    with pytest.raises(CLIConfigureError):
        list(parse_file(str(wrong_file), "csv", False))