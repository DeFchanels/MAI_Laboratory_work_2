import datetime
import logging

from globals import report
from streamstats.errors import IncorrectEventError, UnsupportedTimestampFormatError
from streamstats.models import Event

levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
logger = logging.getLogger(__name__)


def analyser(event_data, file_path, line_number, skip_invalid):
    """
    Accepts an event, the path to the file currently being read, the line number, and a flag of skipping invalid events.
    Analyzes the file and modifies the global report based on the data contained within it.
    """
    if skip_invalid:
        try:
            event = Event.get_event_from_dict(event_data, file_path, line_number)
        except (IncorrectEventError, UnsupportedTimestampFormatError) as err:
            logger.warning(
                f"Skipped invalid event at {file_path}:{line_number} - {err}"
            )
            report['invalid_events_skipped'] += 1
            report['total_events'] += 1
            return 0
    else:
        event = Event.get_event_from_dict(event_data, file_path, line_number)
    report["total_events"] += 1
    report["total_valid_events"] += 1
    if report["first_timestamp"] is None or event.timestamp < datetime.datetime.fromisoformat(report["first_timestamp"].replace('Z', '+00:00')):
        report["first_timestamp"] = event.timestamp.isoformat().replace("+00:00", "Z")
    if report["last_timestamp"] is None or event.timestamp > datetime.datetime.fromisoformat(report["last_timestamp"].replace('Z', '+00:00')):
        report["last_timestamp"] = event.timestamp.isoformat().replace("+00:00", "Z")
    report["sources_counters"][event.source] = report["sources_counters"].get(event.source, 0) + 1
    report["top_errors_sources"][event.source] = report["top_errors_sources"].get(event.source, 0)
    report["levels_counters"][event.level] += 1
    if event.level == "ERROR" or event.level == "CRITICAL":
        report["top_errors_sources"][event.source] += 1
    return 0