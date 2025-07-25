import argparse


def main():
    parser = argparse.ArgumentParser(description="Обработка лог файлов")
    parser.add_argument("--file", nargs="+", required=True, help="Путь к файлу/файлам")
    parser.add_argument(
        "--report", required=True, choices=["average"], help="Тип отчета"
    )
    args = parser.parse_args()
