import json
from typing import List, Dict


def parse_log_files(filepaths: List[str]) -> List[Dict]:
    entries = []
    for filepath in filepaths:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
    return entries
