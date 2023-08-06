import logging

from voluptuous import Any, Optional, Required, Schema

LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def parse_conf(data):
    return main_schema(data)


loggers_schema = Schema({Required("name"): str, Required("level"): Any(*LEVELS.keys())})

outputs_schema = Schema(
    {Optional("file"): str, Optional("stream"): Any("stdout", "stderr")}
)

main_schema = Schema(
    {
        Required("loggers", default=[]): [loggers_schema],
        Required("outputs", default={}): outputs_schema,
    }
)
