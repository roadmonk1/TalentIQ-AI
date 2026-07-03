import logging
import os
from logging.config import dictConfig


def configure_logging():
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
            }
        },
        'loggers': {
            'app.auth': {
                'handlers': ['console'],
                'level': os.getenv('AUTH_LOG_LEVEL', 'INFO').upper(),
                'propagate': False,
            },
            'app': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            }
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    })
