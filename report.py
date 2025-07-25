from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from collections import defaultdict


class Report(ABC):
    @abstractmethod
    def generate(self, entries: List[Dict]) -> List[Tuple[str, int, float]]:
        pass


class AverageReport(Report):
    def generate(self, entries: List[Dict]) -> List[Tuple[str, int, float]]:
        stats = defaultdict(lambda: {"count": 0, "total_time": 0.0})
        for entry in entries:
            url = entry.get("url")
            rt = entry.get("response_time")
            if url is None or rt is None:
                continue
            stats[url]["count"] += 1
            stats[url]["total_time"] += rt

        return sorted(
            [(url, d["count"], d["total_time"] / d["count"]) for url, d in stats.items()],
            key=lambda x: x[1],
            reverse=True
        )
