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
    def __init__(self, log_level, logger_namespace):
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
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
        self.logger = logging.LoggerAdapter(
            logger,
            {"logger_namespace": logger_namespace}
        )
        self.log_level = self.logger.logger.level

    def get_logger(self):
        return self.logger

