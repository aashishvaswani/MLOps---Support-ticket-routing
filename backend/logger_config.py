import logging
from pythonjsonlogger import jsonlogger
import os

def setup_logger():
    log_dir = 'logs'
    log_path = os.path.join(log_dir, 'app.log')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logger = logging.getLogger('ticket_classifier')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_path)
        handler.setLevel(logging.INFO)

        log_format = '%(asctime)s %(levelname)s %(message)s %(endpoint)s %(prediction)s %(method)s %(input)s'
        formatter = jsonlogger.JsonFormatter(log_format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
