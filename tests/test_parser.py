import tempfile
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from log_files_parser import parse_log_files


@pytest.fixture
def log_file():
    data = [
        '{"url": "/api/test", "response_time": 0.5}',
        '{"url": "/api/test", "response_time": 0.6}',
        'invalid json line',
        '{"url": "/api/test", "response_time": 0.8}'
    ]
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    tmp.write("\n".join(data))
    tmp.close()
    yield tmp.name
    os.unlink(tmp.name)


def test_parse_valid_json(log_file):
    """Тестируем валидный json"""
    result = parse_log_files([log_file])
    assert len(result) == 3
    assert all("url" in entry and "response_time" in entry for entry in result)


def test_parse_empty_file():
    """Тестируем пустой файл"""
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    tmp.close()
    try:
        result = parse_log_files([tmp.name])
        assert result == []
    finally:
        os.unlink(tmp.name)
