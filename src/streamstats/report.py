import json
import csv
from globals import report


def make_report(output_file_name):
    """
    Accepts the name of the file where the final report should be saved and saves it there
    """
    with open(f'{output_file_name[:output_file_name.find('.')]}.json', 'w') as f:
        json.dump(report, f, indent=4)
    with open(f'{output_file_name[:output_file_name.find('.')]}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=report.keys())
        writer.writeheader()
        writer.writerow(report)

