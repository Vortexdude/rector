import json
import logging
from typing import Dict, Any

__all__ = ["Logger", "timestamp_log_config"]


def timestamp_log_config(uvicorn_log_config: Dict[str, Any]) -> Dict[str, Any]:
    datefmt = '%d-%m-%Y %H:%M:%S'
    formatters = uvicorn_log_config['formatters']
    formatters['default']['fmt'] = '%(levelprefix)s [%(asctime)s] %(message)s'
    formatters['access']['fmt'] = '%(levelprefix)s [%(asctime)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
    formatters['access']['datefmt'] = datefmt
    formatters['default']['datefmt'] = datefmt
    return uvicorn_log_config


class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """

    def __init__(self, fmt_dict: dict = None, time_format: str = "%d-%d-%y:T%H:%M:%S", msec_format: str = "%s.%03dZ"):
        self.fmt_dict = fmt_dict if fmt_dict else {"message": "message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        """
        Overwritten to look for the attribute in the format dict values instead of the fmt string.
        """
        return 'asctime' in self.fmt_dict.items()

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        KeyError is raised if an unknown attribute is provided in the fmt_dict.
        """
        return {fmt_key: record.__dict__[fmt_value] for fmt_key, fmt_value in self.fmt_dict.items()}

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method, the difference being that a dict is manipulated
        and dumped as JSON instead of a string.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)


class FileFilter(logging.Filter):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def filter(self, record):
        return record.getMessage().startswith(self.string)


class NotFileFilter(logging.Filter):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def filter(self, record):
        return not record.getMessage().startswith(self.string)


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        items = ["message"]  # items to print the in the file
        output = {}
        super(CustomJsonFormatter, self).format(record)
        for key, value in record.__dict__.items():
            if key not in items:
                continue
            if not isinstance(value, dict):
                value = str(value)
                output[key] = value

        return json.dumps(output)


class CustomFormatter(logging.Formatter):
    GREEN = "\x1b[32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    GRAY = "\x1b[38;20m"
    LIGHT_GRAY = "\033[0;37m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    WHITE = "\x1b[0m"
    RESET = "\x1b[0m"

    custom_format = "%(levelname)6s: %(logger_namespace)s %(filename)10s:%(lineno)s - %(message)s"

    FORMATS = {
        logging.DEBUG: BLUE + custom_format + RESET,
        logging.INFO: CYAN + custom_format + RESET,
        logging.WARNING: YELLOW + custom_format + RESET,
        logging.ERROR: RED + custom_format + RESET,
        logging.CRITICAL: BOLD_RED + custom_format + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    def __init__(self, log_level, logger_namespace, logfile=None):
        if log_level is None:
            raise Exception("error: please specify the log level")

        log_levels = {
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warn": logging.WARN,
            "warning": logging.WARNING,
            "info": logging.INFO,
            "debug": logging.DEBUG,
        }
        logger = logging.getLogger(__name__)
        logger.setLevel(log_levels[log_level])
        if logfile:
            fileName = "rector_log"
            file_handler = logging.FileHandler("{0}/{1}.log".format(logfile, fileName))
            file_formatter = CustomJsonFormatter()
            file_handler.setFormatter(file_formatter)
            file_handler.addFilter(FileFilter("logger="))
            logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        console_handler.addFilter(NotFileFilter("logger="))
        logger.addHandler(console_handler)
        self.logger = logging.LoggerAdapter(
            logger,
            {"logger_namespace": logger_namespace}
        )
        self.log_level = self.logger.logger.level

    def get_logger(self):
        return self.logger

