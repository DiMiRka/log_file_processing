import tempfile
import pytest
import os

from src.log_files_parser import parse_log_files


@pytest.fixture
def log_file():
    data = [
        '{"@timestamp": "2025-06-22T13:57:32+00:00", "url": "/test/1", "response_time": 0.1}',
        '{"@timestamp": "2025-06-23T14:00:00+00:00", "url": "/test/2", "response_time": 0.2}',
        '{"@timestamp": "2025-06-22T15:00:00+00:00", "url": "/test/3", "response_time": 0.3}',
    ]
    tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    tmp.write("\n".join(data))
    tmp.close()
    yield tmp.name
    os.unlink(tmp.name)


def test_parse_valid_json(log_file):
    result = parse_log_files([log_file])
    assert len(result) == 3
    assert all("url" in entry and "response_time" in entry for entry in result)


def test_parse_empty_file():
    tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
    tmp.close()
    try:
        result = parse_log_files([tmp.name])
        assert result == []
    finally:
        os.unlink(tmp.name)


@pytest.mark.parametrize(
    "date_filter, expected_urls",
    [
        ("2025-06-22", ["/test/1", "/test/3"]),
        ("2025-06-23", ["/test/2"]),
        ("2025-06-24", []),
        ("2099-01-01", []),
        (None, ["/test/1", "/test/2", "/test/3"]),
    ],
)
def test_parse_date_filter(log_file, date_filter, expected_urls):
    result = parse_log_files([log_file], date_filter=date_filter)
    urls = [entry["url"] for entry in result]
    assert sorted(urls) == sorted(expected_urls)


def test_parse_date_filter_invalid_date(log_file):
    with pytest.raises(ValueError, match="Не верный формат даты"):
        parse_log_files([log_file], date_filter="not-a-date")
