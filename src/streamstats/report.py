import csv
import json

from globals import report


def make_report(output_file_name):
    """
    Accepts the name of the file where the final report should be saved and saves it there
    """
    if '.' in output_file_name:
        file_name = output_file_name[:output_file_name.find('.')]
    else:
        file_name = output_file_name
    with open(f'{file_name}.json', 'w') as f:
        json.dump(report, f, indent=4)
    with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=report.keys())
        writer.writeheader()
        writer.writerow(report)

