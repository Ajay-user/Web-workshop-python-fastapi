
import json
from datetime import datetime, timezone

import logging
from logging import Formatter



class JsonFormatter(Formatter):
    def format(self, record):

        entry = {
            # 'timestamp': str(datetime.now(tz=timezone.utc)),
            'timestamp': datetime.now(tz=timezone.utc).isoformat(), # Return the time formatted according to ISO.  [ string ]
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage()
        }

        return json.dumps(entry)
    

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

streamer = logging.StreamHandler()
streamer.setLevel(logging.INFO)
streamer.setFormatter(JsonFormatter())

logger.addHandler(streamer)


logger.info("Hello ... this is logging 101")