import pytest
from globals import report
from streamstats.analysis import analyser


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


def test_only_event():
    event_data = {
        "timestamp": "2026-10-09T10:00:00Z",
        "level": "INFO",
        "source": "auth",
        "message": "Log in"
    }
    analyser(event_data, "input.jsonl", 1, False)
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
            "auth": 1
        },
        "top_errors_sources": {
            "auth": 0
        },
        "first_timestamp": "2026-10-09T10:00:00Z",
        "last_timestamp": "2026-10-09T10:00:00Z",
        "invalid_events_skipped": 0
    }
    assert report == expected_result


def test_multiple_events():
    event_1 = {"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}
    event_2 = {"timestamp": "2026-10-09T08:00:00Z", "level": "ERROR", "source": "reg", "message": ""}
    event_3 = {"timestamp": "2026-10-09T15:00:00Z", "level": "WARNING", "source": "web", "message": ""}
    for n, event in enumerate([event_1, event_2, event_3]):
        analyser(event, "input.jsonl", n, False)
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
    assert report == expected_result


def test_skip_sole_invalid_enabled():
    event = {"level": "INVALID", "source": ""}  # Невалидное событие (нет timestamp, нет message, source пустой, уровень недоступен
    analyser(event, "input.jsonl", 1, True)
    expected_result = {
        "total_events": 1,
        "total_valid_events": 0,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        },
        "sources_counters": {},
        "top_errors_sources": {},
        "first_timestamp": None,
        "last_timestamp": None,
        "invalid_events_skipped": 1
    }
    assert report == expected_result


def test_skip_multiple_events_and_invalid_enabled():
    event_1 = {"level": "INVALID", "source": ""}  # Невалидное событие (нет timestamp, нет message, source пустой, уровень недоступе
    event_2 = {"timestamp": "2026-10-09T12:00:00Z", "level": "INFO", "source": "auth", "message": ""}
    event_3 = {"timestamp": "2026-10-09T08:00:00Z", "level": "ERROR", "source": "reg", "message": ""}
    for n, event in enumerate([event_1, event_2, event_3]):
        analyser(event, "input.jsonl", n, True)
    expected_result = {
        "total_events": 3,
        "total_valid_events": 2,
        "levels_counters": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 1,
            "CRITICAL": 0
        },
        "sources_counters": {
            "auth": 1,
            "reg": 1
        },
        "top_errors_sources": {
            "reg": 1,
            "auth": 0
        },
        "first_timestamp": "2026-10-09T08:00:00Z",
        "last_timestamp": "2026-10-09T12:00:00Z",
        "invalid_events_skipped": 1
    }
    assert report == expected_result