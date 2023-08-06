import os
import sys

from .settings import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        # 'mail_admins': {
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'level': 'ERROR',
        #      # But the emails are plain text by default - HTML is nicer
        #     'include_html': True,
        # },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, 'output.log'),
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'logingovpl': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
