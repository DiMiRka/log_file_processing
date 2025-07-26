import pytest
from src.report import AverageReport


@pytest.mark.parametrize(
    "entries, expected",
    [
        (
            [
                {"url": "/test/1", "response_time": 0.1},
                {"url": "/test/1", "response_time": 0.3},
                {"url": "/test/2", "response_time": 0.2},
                {"url": "/test/2", "response_time": 0.4},
                {"url": "/test/3", "response_time": 0.5},
            ],
            [
                ("/test/1", 2, 0.2),
                ("/test/2", 2, 0.3),
                ("/test/3", 1, 0.5),
            ],
        ),
        (
            [],
            [],
        ),
        (
            [
                {"url": "/test/single", "response_time": 1.0},
            ],
            [
                ("/test/single", 1, 1.0),
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
