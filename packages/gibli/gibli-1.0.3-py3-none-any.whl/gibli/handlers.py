from logging import StreamHandler
from logging.handlers import WatchedFileHandler


class GibliHandler:
    pass


class GibliWatchedFileHandler(GibliHandler, WatchedFileHandler):
    pass


class GibliStreamHandler(GibliHandler, StreamHandler):
    pass
