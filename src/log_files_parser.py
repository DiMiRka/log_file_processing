import json
from typing import List, Dict


def parse_log_files(file_paths: List[str], date_filter: str = None) -> List[Dict]:
    result = []
    for filepath in file_paths:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                try:
                    log_line = json.loads(line)
                    timestamp = log_line.get("@timestamp")
                    if date_filter and timestamp:
                        log_date = timestamp[:10]
                        if log_date != date_filter:
                            continue
                    result.append(log_line)
                except json.JSONDecodeError:
                    continue
    return result
