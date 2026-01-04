import logging
from logging import config


CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters':{
        'detailed': {
            'format': "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },

    'handlers':{
        'console':{
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'INFO'
        },
        'file':{
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename':'./Scripts/test_log_config.log',
            'level': 'DEBUG'
        }
    },

    'loggers': {

        'myapp':{

            'handlers': ['console', 'file'],
            'level':"DEBUG",
            'propagate':False
        }

    }

}



config.dictConfig(CONFIG)

logger = logging.getLogger('myapp')

logger.info("Logging 101")