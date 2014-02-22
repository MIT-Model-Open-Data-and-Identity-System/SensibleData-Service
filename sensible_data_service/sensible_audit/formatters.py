import logging

from bson.timestamp import Timestamp
from pymongo import Connection
from pymongo.collection import Collection
from pymongo.errors import OperationFailure, PyMongoError

class AuditorFormatter(logging.Formatter):

    DEFAULT_PROPERTIES = logging.LogRecord('', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            'timestamp': Timestamp(int(record.created), int(record.msecs)),
            'level': record.levelname,
            #'thread': record.thread,
            #'threadName': record.threadName,
            'message': record.getMessage(),
            'loggerName': record.name,
            #'fileName': record.pathname,
            'module': record.module,
            'method': record.funcName,
            #'lineNumber': record.lineno
        }
        
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document