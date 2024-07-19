import sys
import logging
from app.core.config import settings

logging_mapping = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
}


logging_string = "[%(levelname)s] %(asctime)s %(name)s: %(message)s"
logger = logging.getLogger(settings.PROJECT_NAME)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(logging_string)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


