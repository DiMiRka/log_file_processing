import argparse
from tabulate import tabulate

from src.log_files_parser import parse_log_files
from src.report import AverageReport
from src.exceptions import InvalidReportTypeError


def main():
    parser = argparse.ArgumentParser(description="Обработка лог файлов")
    parser.add_argument("--file", nargs="+", required=True, help="Путь к файлу/файлам")
    parser.add_argument("--report", required=True, choices=["average"], help="Тип отчета")
    parser.add_argument("--date", help="Фильтр по дате лога (YYYY-MM-DD)")
    args = parser.parse_args()

    entries = parse_log_files(args.file, args.date)

    if args.report == "average":
        report = AverageReport()
        report_data = report.generate(entries)
    else:
        raise InvalidReportTypeError(f"Отчет типа '{args.report}' не поддерживается")

    print(
        tabulate(
            report_data,
            headers=["handler", "total", "avg_response_time"],
            floatfmt=".3f",
        )
    )


if __name__ == "__main__":
    main()
