import json
from datetime import datetime
from logging import Formatter

IGNORE_FIELDS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
}


class JsonFormatter(Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)

    def format(self, r):
        res = {
            "level": getattr(r, "levelname"),
            "created": datetime.fromtimestamp(getattr(r, "created"))
            .astimezone()
            .isoformat(),
            "message": r.getMessage(),
            "line": f"{r.filename}:{r.lineno}",
        }

        for name in r.__dict__:
            if name not in IGNORE_FIELDS:
                res[name] = getattr(r, name)

        if r.exc_info:
            res["exception"] = self.formatException(r.exc_info)

        return json.dumps(res)
