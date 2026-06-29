class AppError(Exception):
    pass


class InvalidRowError(AppError):
    pass


class DownloadReportError(AppError):
    pass


class TableFormatError(AppError):
    pass
