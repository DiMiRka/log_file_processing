import json
from typing import List, Dict
from datetime import datetime


def parse_log_files(files: List[str], date_filter: str = None) -> List[Dict]:
    result = []

    if date_filter:
        try:
            date_log_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Не верный формат даты: {date_filter}. Верный YYYY-MM-DD.")
    else:
        date_log_filter = None

    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                try:
                    log_line = json.loads(line)
                    if date_log_filter:
                        ts = log_line.get("@timestamp")
                        if not ts:
                            continue
                        try:
                            date_log = datetime.fromisoformat(ts.replace("Z", "+00:00")).date()
                        except ValueError:
                            continue
                        if str(date_log) != date_filter:
                            continue
                    result.append(log_line)
                except json.JSONDecodeError:
                    continue
    return result
