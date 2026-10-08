import argparse
import sys

from streamstats.analysis import analyser
from streamstats.errors import StreamStatsError
from streamstats.parsers import parse_file


def main():
    parser = argparse.ArgumentParser(description='Потоковый анализатор файлов (CSV|JSONL)')
    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help='Доступные команды'
    )
    analyze_parser = subparsers.add_parser('analyze', help='Анализ файла и генерация отчета')
    analyze_parser.add_argument('inputs', nargs='+', help="Пути к входным файлам")
    analyze_parser.add_argument('--format', choices=['csv', 'jsonl'], required=True, help="Формат входных файлов")
    analyze_parser.add_argument('--skip-invalid', action='store_true', help="Пропуск невалидных строк вместо завершения с кодом ошибки")
    analyze_parser.add_argument('--output', default="output.json", help="Путь для сохранения итогового JSON отчета (по умолчанию - output.json)")
    args = parser.parse_args()
    try:
        events = []
        skipped_events = 0
        for file_path in args.inputs:
            events, skipped_events = parse_file(file_path, args.format, events, args.skip_invalid)
        analyser(events, skipped_events, args.output)
    except StreamStatsError as error:
        print(f"{error}")
        sys.exit(2)

if __name__ == "__main__":
    main()