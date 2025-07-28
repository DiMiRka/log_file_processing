from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from collections import defaultdict

from src.logger import logger


class Report(ABC):
    @abstractmethod
    def generate(self, entries: List[Dict]) -> List[Tuple[str, int, float]]:
        pass


class AverageReport(Report):
    def generate(self, entries: List[Dict]) -> List[Tuple[str, int, float]]:
        stats = defaultdict(lambda: {"count": 0, "total_time": 0.0})
        skipped = 0
        count = 0
        for idx, entry in enumerate(entries):
            count += 1
            url = entry.get("url")
            rt = entry.get("response_time")
            if url is None or rt is None:
                logger.warning(
                    f"Пропущена запись {idx + 1}: отсутствует 'url' или 'response_time'"
                )
                skipped += 1
                continue
            stats[url]["count"] += 1
            stats[url]["total_time"] += rt

        logger.info(
            f"""Сформирован отчёт общего количества и среднему времени ответа эндопоинтов.
        Обработано {count} записей, пропущено: {skipped}"""
        )

        return sorted(
            [(url, d["count"], d["total_time"] / d["count"]) for url, d in stats.items()],
            key=lambda x: x[1],
            reverse=True,
        )
