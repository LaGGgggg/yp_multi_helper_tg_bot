from logging import getLogger
from logging.config import dictConfig

from settings import WARNING_LOG_FILE_PATH, INFO_LOG_FILE_PATH


dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main': {
            'format': '[{levelname}] [{asctime}] path - "{pathname}" function - "{funcName}" message - "{message}"',
            'style': '{',
        },
        'short': {
            'format': '[{levelname}] [{asctime}] message - "{message}"',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'short',
        },
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'main',
            'filename': WARNING_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 10,  # 10 Mb
            'encoding': 'utf-8',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'main',
            'filename': INFO_LOG_FILE_PATH,
            'maxBytes': 1024 * 1024 * 10,  # 10 Mb
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console', 'file_warning', 'file_info'],
            'level': 'INFO',
        },
    },
})


def get_logger(name):
    return getLogger(name)
