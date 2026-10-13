import argparse
import logging
import sys

from globals import report
from streamstats.analysis import analyser
from streamstats.errors import StreamStatsError
from streamstats.parsers import parse_file
from streamstats.report import make_report


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s"
    )
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
        for file_path in args.inputs: # Цикл по всем файлам
            for event, line_number in parse_file(file_path, args.format, args.skip_invalid): # Проходим отдельно по каждому событию в файле
                analyser(event, file_path, line_number, args.skip_invalid) # Анализируем событие
        top_5_errors_sources = dict(sorted(report["top_errors_sources"].items(), key=lambda x: x[1], reverse=True)[:5])
        report["top_errors_sources"] = top_5_errors_sources
        make_report(args.output)  # Записываем отчет в output файл
    except StreamStatsError as error:
        top_5_errors_sources = dict(sorted(report["top_errors_sources"].items(), key=lambda x: x[1], reverse=True)[:5])
        report["top_errors_sources"] = top_5_errors_sources
        make_report(args.output)
        print(f"{error}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()