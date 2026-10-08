import csv, json
from streamstats.errors import UnsupportedFileFormatError, CLIConfigureError
from models import Event


def parse_file(file_path, file_format):
    events = []
    try:
        with open(file_path, 'r') as file:
            if file_format == "csv":  # Если введенный тип файла
                reader = csv.DictReader(file, strict=True)
                for line in reader:
                    event_data = line
                    event = Event.get_event_from_dict(event_data)
                    events.append(event)
            elif file_format == "json":
                try:
                    for line in file:
                        event_data = json.loads(line)
                        event = Event.get_event_from_dict(event_data)
                        events.append(event)
                except json.decoder.JSONDecodeError:
                    raise CLIConfigureError(f"Error occurred while reading a file: {file_format}")
            else:
                raise UnsupportedFileFormatError(f"Invalid file format: {file_format}")
    except FileNotFoundError:
        raise CLIConfigureError(f"File not found: {file_path}")
    print(events)
    return events

parse_file("input.csv", "json")