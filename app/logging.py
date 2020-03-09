# import logging
#
# import decouple
# import structlog
# from gunicorn import glogging
#
# processors = [
#     structlog.stdlib.add_log_level,
#     structlog.stdlib.PositionalArgumentsFormatter(),
#     structlog.processors.TimeStamper(fmt="iso"),
#     structlog.processors.JSONRenderer(sort_keys=True),
# ]
# if decouple.config("DEBUG", default=False):
#     processors.extend(
#         [
#             structlog.processors.StackInfoRenderer(),
#             structlog.processors.format_exc_info,
#         ]
#     )
# BaseLogger = structlog.wrap_logger(structlog.get_logger(), processors=processors,)


# class BaseLogger:
#     @property
#     def _logger(self):
#         if not getattr(self, "__logger__", None):
#             processors = [
#                 structlog.stdlib.add_log_level,
#                 structlog.stdlib.PositionalArgumentsFormatter(),
#                 structlog.processors.TimeStamper(fmt="iso"),
#                 structlog.processors.JSONRenderer(sort_keys=True),
#             ]
#             if decouple.config("DEBUG", default=False):
#                 processors.extend([
#                     structlog.processors.StackInfoRenderer(),
#                     structlog.processors.format_exc_info,
#                 ])
#             self.__logger__ = structlog.wrap_logger(
#                 structlog.get_logger(),
#                 processors=processors,
#             )
#         return self.__logger__
#
#     def bind(self, **kwargs):
#         self._logger = self._logger.bind(**kwargs)
#         return self
#
#     def unbind(self, *keys):
#         self._logger = self._logger.unbind(*keys)
#         return self
#
#     def _can_log(self, level):
#         if level < self.level:
#             return False
#         return True
#
#     def log(self, lvl, msg, *args, **kwargs) -> None:
#         if lvl < self.level:
#             return
#         self._logger.log(lvl, msg, *args, **kwargs)
#
#     def critical(self, msg, *args, **kwargs) -> None:
#         if self._can_log(logging.CRITICAL):
#             self._logger.error(msg, *args, **kwargs)
#
#     def error(self, msg, *args, **kwargs) -> None:
#         if self._can_log(logging.ERROR):
#             self._logger.error(msg, *args, **kwargs)
#
#     def warning(self, msg, *args, **kwargs) -> None:
#         if self._can_log(logging.WARNING):
#             self._logger.warning(msg, *args, **kwargs)
#
#     def info(self, msg, *args, **kwargs) -> None:
#         if self._can_log(logging.INFO):
#             self._logger.info(msg, *args, **kwargs)
#         # self.log(logging.INFO, msg, *args, **kwargs)
#
#     def debug(self, msg, *args, **kwargs) -> None:
#         if self._can_log(logging.DEBUG):
#             self._logger.debug(msg, *args, **kwargs)
#
#     def exception(self, msg, *args, **kwargs) -> None:
#         if self._can_log(logging.ERROR):
#             self._logger.exception(msg, *args, **kwargs)


# class Logger(BaseLogger):
#     def __init__(self, level=logging.INFO):
#         self.level = level


# class GunicornLogger(BaseLogger, glogging.Logger):
#     def __init__(self, cfg={}):
#         super(GunicornLogger, self).__init__(cfg)
#         # self.error_log.propagate = True
#         # self.access_log.propagate = True
#         # self.error_log = self._logger
#         # self.access_log = self._logger
#         # self.level = logging.INFO
#
#     def access(self, resp, req, environ, request_time):
#         """Overrided method to ensure access is always logged."""
#         desired_environment = [
#             "HTTP_COOKIE",
#             "HTTP_HOST",
#             "HTTP_USER_AGENT",
#             "HTTP_X_FORWARDED_FOR",
#             "HTTP_X_REAL_IP",
#             "PATH_INFO",
#             "QUERY_STRING",
#             "RAW_URI",
#             "REMOTE_ADDR",
#             "REMOTE_PORT",
#             "REQUEST_METHOD",
#             "SCRIPT_NAME",
#             "SERVER_NAME",
#             "SERVER_PORT",
#             "SERVER_PROTOCOL",
#             "SERVER_SOFTWARE",
#         ]
#         self.access_log.info(
#             "REQUEST",
#             **{
#                 "environ": {
#                     k: v for k, v in environ.items() if k in desired_environment
#                 },
#                 "duration": request_time,
#             },
#         )
#
#     def reopen_files(self):
#         pass
#
#     def close_on_exec(self):
#         pass
