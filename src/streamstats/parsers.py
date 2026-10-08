import csv, json
from streamstats.errors import UnsupportedFileFormatError, CLIConfigureError, IncorrectEventError
from streamstats.models import Event
from pathlib import Path


def parse_file(file_path, file_format, events, skip_invalid):
    skipped_events = 0
    try:
        with open(file_path, 'r') as file:
            if file_format == "csv": # Если введенный тип файла csv
                if Path(file_path).suffix.lower() == ".csv":
                    reader = csv.DictReader(file, strict=True)
                    for number, line in enumerate(reader, 1):
                        event_data = line
                        if skip_invalid:
                            try:
                                event = Event.get_event_from_dict(event_data, file_path, number)
                                events.append(event)
                            except IncorrectEventError:
                                skipped_events += 1
                        else:
                            event = Event.get_event_from_dict(event_data, file_path, number)
                            events.append(event)
                else:
                    raise CLIConfigureError(f"File type is not csv: {file_path}")
            elif file_format == "jsonl":
                try:
                    for number, line in enumerate(file, 1):
                        event_data = json.loads(line)
                        if skip_invalid:
                            try:
                                event = Event.get_event_from_dict(event_data, file_path, number)
                                events.append(event)
                            except IncorrectEventError:
                                skipped_events += 1
                        else:
                            event = Event.get_event_from_dict(event_data, file_path, number)
                            events.append(event)
                except json.decoder.JSONDecodeError:
                    raise CLIConfigureError(f"Error occurred while reading a file: {file_path}")
            else:
                raise UnsupportedFileFormatError(f"Invalid file format: {file_format}")
    except FileNotFoundError:
        raise CLIConfigureError(f"File not found: {file_path}")
    return events, skipped_events