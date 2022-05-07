from app.config import get_settings

settings = get_settings()
LOGLEVEL = settings.LOG_LEVEL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(process)d:%(name)s:%(lineno)s] - [%(module)s:%(funcName)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': LOGLEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/usr/src/app/logs/app.log',
            'formatter': 'standard',
            'maxBytes': 1048576, 
            'backupCount': 5
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'models': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        'test': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'main': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        'router': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        'uvicorn': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        'fixtures': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },
        'crud': {
            'handlers': ['file'],
            'level': LOGLEVEL,
            'propagate': True,
        },

    },
}
