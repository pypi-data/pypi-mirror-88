import logging
import os
import pathlib
import sys

from .conf import LEVELS, parse_conf
from .formatters import JsonFormatter
from .handlers import GibliHandler, GibliStreamHandler, GibliWatchedFileHandler

"""
Configuration example:

{
    "loggers": [
        {"name": "foo", "level": "info"},
        {"name": "bar", "level": "warning"},
    ],
    "outputs": {
        "file": "/var/log/baz.log",
        "stream": "stderr",
    }
}
"""


def configure_logging(conf):
    conf = parse_conf(conf)

    loggers = conf["loggers"]
    outputs = conf.get("outputs", {})
    file = outputs.get("file")
    stream = outputs.get("stream")

    if file:
        path, _ = os.path.split(file)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    if stream:
        if stream == "stdout":
            stream = sys.stdout
        else:
            stream = sys.stderr
    elif file is None:
        stream = sys.stderr

    # levels

    # set
    for logger in loggers:
        name = logger["name"]
        level = LEVELS[logger["level"]]
        logging.getLogger(name).setLevel(level)
    # reset others
    for name, logger in getattr(logging.root, "manager").loggerDict.items():
        found = False
        for logger2 in loggers:
            if logger2["name"] == name:
                found = True
                break
        if not found:
            try:
                logger.setLevel(logging.NOTSET)
            except AttributeError:
                pass  # AttributeError: 'PlaceHolder' object has no attribute 'setLevel'

    # handlers

    handlers = []
    if file:
        handlers.append(GibliWatchedFileHandler(file))
    if stream:
        handlers.append(GibliStreamHandler(stream))

    if handlers:
        json_formatter = JsonFormatter()
        for handler in handlers:
            handler.setFormatter(json_formatter)

    for handler in handlers:
        logging.root.addHandler(handler)

    # remove other handlers
    for handler in logging.root.handlers.copy():
        if isinstance(handler, GibliHandler) and handler not in handlers:
            logging.root.removeHandler(handler)
            handler.close()
