import json
import multiprocessing
import os
import pathlib

import decouple
import structlog

# from app.logging import GunicornLogger

is_development = decouple.config(
    "DEBUG",
    default=bool(
        os.path.exists(pathlib.Path(__file__).parent.parent.absolute() / ".env")
    ),
)
cpu_reservation = decouple.config(
    "CPU_RESERVATION", default=multiprocessing.cpu_count() * 1024, cast=int
)
workers_per_core = decouple.config("WORKERS_PER_CORE", default=4, cast=int)
host = decouple.config("HOST", default="0.0.0.0")
port = decouple.config("PORT", default="80")

workers = int(
    1 if is_development else (cpu_reservation // (1024 / workers_per_core)) + 1
)
bind = [f"{host}:{port}"]
keepalive = 120

# Enable configuration of gunicorn via enviroment variables.
_from_env = {}
for k, v in os.environ.items():
    if k.startswith("GUNICORN_"):
        key = k.split("_", 1)[1].lower()
        _from_env[key] = v
        locals()[key] = v

print(
    json.dumps(
        {
            "workers": workers,
            "bind": bind,
            **_from_env,
            # Additional, non-gunicorn variables
            "is_development": is_development,
            "cpu_reservation": cpu_reservation,
            "workers_per_core": workers_per_core,
            "host": host,
            "port": port,
        }
    )
)

loglevel = 'info'
errorlog = '-'
accesslog = '-'


# logger_class=GunicornLogger

# https://albersdevelopment.net/2019/08/15/using-structlog-with-gunicorn/
# processors = [
#     structlog.stdlib.add_log_level,
#     structlog.stdlib.add_logger_name,
#     structlog.stdlib.PositionalArgumentsFormatter(),
#     structlog.processors.TimeStamper(fmt="iso"),
#     # structlog.processors.JSONRenderer(sort_keys=True),
# ]
# if is_development:
#     processors.extend(
#         [
#             structlog.processors.StackInfoRenderer(),
#             structlog.processors.format_exc_info,
#         ]
#     )
# logconfig_dict = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "json": {
#             "()": structlog.stdlib.ProcessorFormatter,
#             "processor": structlog.processors.JSONRenderer(sort_keys=True),
#             "foreign_pre_chain": processors,
#         }
#     },
#     # "root": {"level": "INFO", "handlers": ["console"]},
#     "handlers": {
#         "console": {"class": "logging.StreamHandler", "formatter": "json"},
#     },
#     "loggers": {
#         "": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             # "propagate": True,
#         },
#         "gunicorn.error": {
#             "handlers": ["console"],
#             "level": "INFO",
#         },
#         "uvicorn.error": {
#             "handlers": ["console"],
#             "level": "INFO",
#         },
#         "uvicorn.access": {
#             "handlers": ["console"],
#             "level": "INFO",
#         },
#     },
# }
