import json
from typing import List, Dict
from datetime import datetime

from src.logger import logger


def parse_log_files(files: List[str], date_filter: str = None) -> List[Dict]:
    result = []

    if date_filter:
        try:
            date_log_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Не верный формат даты: {date_filter}. Верный YYYY-MM-DD.")
    else:
        date_log_filter = None

    for idx, file in enumerate(files):
        skipped = 0
        try:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    try:
                        log_line = json.loads(line)
                        if date_log_filter:
                            ts = log_line.get("@timestamp")
                            if not ts:
                                logger.warning(
                                    f"Пропущена строка {idx} в {file}: отсутствует '@timestamp'"
                                )
                                skipped += 1
                                continue
                            try:
                                date_log = datetime.fromisoformat(
                                    ts.replace("Z", "+00:00")
                                ).date()
                            except ValueError:
                                logger.warning(
                                    f"Пропущена строка {idx} в {file}: некорректный формат времени '@timestamp': {ts}"
                                )
                                skipped += 1
                                continue
                            if str(date_log) != date_filter:
                                continue
                        result.append(log_line)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Невалидный JSON в файле {file}, строка {idx}: {e}")
                        skipped += 1
                        continue
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file}")
        except Exception as e:
            logger.exception(f"Ошибка при обработке файла {file}: {e}")

        logger.info(f"parser.py Обработано {len(result)} записей, пропущено: {skipped}")

    return result
