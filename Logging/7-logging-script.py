import logging
import json





# Determine if the specified record is to be logged.
# Returns True if the record should be logged, or False otherwise. If deemed appropriate, the record may be modified in-place
class CustomFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'username'):
            record.username = 'John Doe'
        if not hasattr(record, 'user_id'):
            record.user_id = '1AA12'
        if hasattr(record, 'anonymize'):
            if record.anonymize:
                del record.user_id
                del record.username
        return True

class CustomFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            'level': record.levelname,
            'file': record.filename,
            'user_id':{
                'name' : record.username if hasattr(record, 'username') else 'Not mentioned',
                'id_number': record.user_id if hasattr(record, 'user_id') else 'Not mentioned'
            },
            'message': record.getMessage()
        }        

        return json.dumps(entry)




logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


streamer = logging.StreamHandler()
streamer.setLevel(logging.INFO)
streamer.addFilter(CustomFilter())
streamer.setFormatter(CustomFormatter())


logger.addHandler(streamer)




logger.info("Hello this is logging 101")
# o/p : {"level": "INFO", "file": "7-logging-script.py", "user_id": {"name": "John Doe", "id_number": "1AA12"}, "message": "Hello this is logging 101"}

logger.info("Hello from logging", extra={'username':'Ajay', 'user_id':'42F'})
# {"level": "INFO", "file": "7-logging-script.py", "user_id": {"name": "Ajay", "id_number": "42F"}, "message": "Hello from logging"}

logger.info("Hello from logging", extra={'username':'Ajay', 'user_id':'42F', 'anonymize':True})
# {"level": "INFO", "file": "7-logging-script.py", "user_id": {"name": "Not mentioned", "id_number": "Not mentioned"}, "message": "Hello from logging"}