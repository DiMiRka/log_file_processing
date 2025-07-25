import pytest
from src.report import AverageReport


@pytest.mark.parametrize(
    "entries, expected",
    [
        (
            [
                {"url": "/api/test1", "response_time": 0.1},
                {"url": "/api/test1", "response_time": 0.3},
                {"url": "/api/test2", "response_time": 0.2},
                {"url": "/api/test2", "response_time": 0.4},
                {"url": "/api/test3", "response_time": 0.5},
            ],
            [
                ("/api/test1", 2, 0.2),
                ("/api/test2", 2, 0.3),
                ("/api/test3", 1, 0.5),
            ],
        ),
        (
            [],
            [],
        ),
        (
            [
                {"url": "/api/single", "response_time": 1.0},
            ],
            [
                ("/api/single", 1, 1.0),
            ],
        ),
    ],
)
def test_average_report(entries, expected):
    report = AverageReport()
    result = report.generate(entries)

    assert len(result) == len(expected)

    for actual, exp in zip(result, expected):
        assert actual[0] == exp[0]  # handler
        assert actual[1] == exp[1]  # total
        assert round(actual[2], 1) == exp[2]  # avg_response_time
