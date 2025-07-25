import argparse
import sys
from tabulate import tabulate
from parser import parse_log_files
from report import AverageReport


def main():
    parser = argparse.ArgumentParser(description="Обработка лог файлов")
    parser.add_argument("--file", nargs="+", required=True, help="Путь к файлу/файлам")
    parser.add_argument(
        "--report", required=True, choices=["average"], help="Тип отчета"
    )
    args = parser.parse_args()
    entries = parse_log_files(args.file)

    if args.report == "average":
        report = AverageReport()
        report_data = report.generate(entries)
    else:
        pass

    print(
        tabulate(
            report_data,
            headers=["Endpoint", "Requests", "Avg. Response Time"],
            floatfmt=".3f",
        )
    )


if __name__ == "__main__":
    main()
