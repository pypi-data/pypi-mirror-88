import logging

from .handlers import GibliHandler


class ContextFilter(logging.Filter):
    def __init__(self, name, data):
        if not name:
            raise ValueError("Name for context filter must be provided")
        if not data:
            raise ValueError("Data for context filter must be provided")
        self._name = name
        self._data = data

    def filter(self, record):
        setattr(record, self._name, self._data)
        return True

    def __enter__(self):
        for handler in logging.root.handlers:
            if isinstance(handler, GibliHandler):
                handler.addFilter(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for handler in logging.root.handlers:
            if isinstance(handler, GibliHandler):
                handler.removeFilter(self)
