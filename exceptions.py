class LogReportError(Exception):
    """Базовое исключение."""


class InvalidReportTypeError(LogReportError):
    """Неподдерживаемый тип отчета"""
