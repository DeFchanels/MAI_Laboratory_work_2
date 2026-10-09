import pytest
from datetime import datetime, timezone
from streamstats.models import Event
from streamstats.errors import IncorrectEventError, UnsupportedTimestampFormatError


def test_event_valid_creation(): # Обычный случай
    event = {
        "timestamp": "2026-10-09T10:00:00Z",
        "level": "INFO",
        "source": "auth",
        "message": "Log in"
    }
    event = Event.get_event_from_dict(event, "input.jsonl", 1)

    assert event.level == "INFO"
    assert event.source == "auth"
    assert event.message == "Log in"
    assert event.timestamp == datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)


def test_event_valid_creation_with_russian(): # Обычный случай 2 (С русским словом)
    event = {
        "timestamp": "2026-10-09T10:00:00Z",
        "level": "CRITICAL",
        "source": "Аутентификатор",
        "message": ""
    }
    event = Event.get_event_from_dict(event, "input.jsonl", 1)

    assert event.level == "CRITICAL"
    assert event.source == "Аутентификатор"
    assert event.message == ""
    assert event.timestamp == datetime(2026, 10, 9, 10, 0, 0, tzinfo=timezone.utc)


def test_missing_field(): # У события отсутствует обязательное поле
    data = {
        "level": "ERROR",
        "source": "auth",
        "message": ""
    }
    with pytest.raises(IncorrectEventError):
        Event.get_event_from_dict(data, "input.jsonl", 1)


def test_invalid_level(): # У события недопустимый уровень
    data = {
        "timestamp": "2026-10-09T10:00:00Z",
        "level": "FIRST",
        "source": "auth",
        "message": ""
    }
    with pytest.raises(IncorrectEventError):
        Event.get_event_from_dict(data, "input.jsonl", 1)


def test_empty_source(): # У события пустой источник
    event = {
        "timestamp": "2026-10-09T10:00:00Z",
        "level": "CRITICAL",
        "source": "",
        "message": "Log in"
    }
    with pytest.raises(IncorrectEventError):
        event = Event.get_event_from_dict(event, "input.jsonl", 1)


def test_empty_source_2(): # У события пустой источник (только из пробелов)
    event = {
        "timestamp": "2026-10-09T10:00:00Z",
        "level": "CRITICAL",
        "source": "    ",
        "message": "Log in"
    }
    with pytest.raises(IncorrectEventError):
        event = Event.get_event_from_dict(event, "input.jsonl", 1)


def test_invalid_timestamp(): # У события недопустимый формат временной метки
    data = {
        "timestamp": "2022",
        "level": "INFO",
        "source": "auth",
        "message": ""
    }
    with pytest.raises(UnsupportedTimestampFormatError):
        Event.get_event_from_dict(data, "input.jsonl", 1)