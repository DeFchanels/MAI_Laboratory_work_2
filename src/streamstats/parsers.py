import csv
import json
import logging
from pathlib import Path

from globals import report
from streamstats.errors import (
    CLIConfigureError,
    IncorrectEventError,
    UnsupportedFileFormatError,
)

logger = logging.getLogger(__name__)


def parse_file(file_path, file_format, skip_invalid):
    try:
        with open(file_path, 'r') as file:
            if file_format == "csv": # Если введенный тип файла csv
                if Path(file_path).suffix.lower() == ".csv":
                    reader = csv.DictReader(file, strict=True)
                    for number, line in enumerate(reader, 2):
                        event_data = line
                        yield event_data, number
                else:
                    raise CLIConfigureError(f"File type is not csv: {file_path}")
            elif file_format == "jsonl": # Если введенный тип файла jsonl
                if Path(file_path).suffix.lower() == ".jsonl":
                    for number, line in enumerate(file, 1):
                        try:
                            event_data = json.loads(line)
                            yield event_data, number
                        except json.decoder.JSONDecodeError:
                            if not skip_invalid:
                                raise IncorrectEventError(
                                    f"Error occurred while reading a file line: {file_path}, line: {number}")
                            else:
                                logger.warning(
                                    f"Error occurred while reading a file line: {file_path}, line: {number}"
                                )
                                report["invalid_events_skipped"] += 1
                                report["total_events"] += 1
                else:
                    raise CLIConfigureError(f"File type is not jsonl: {file_path}")
            else:
                raise UnsupportedFileFormatError(f"Invalid file format: {file_format}")
    except FileNotFoundError:
        raise CLIConfigureError(f"File not found: {file_path}")
