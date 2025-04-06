import logging
from pythonjsonlogger import jsonlogger #type: ignore
import os

def setup_logger():
    log_dir = 'logs'
    log_path = os.path.join(log_dir, 'app.log')

    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger('ticket_classifier')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)

        stdout_handler = logging.StreamHandler()

        log_format = '%(asctime)s %(levelname)s %(message)s %(endpoint)s %(prediction)s %(method)s %(input)s'
        formatter = jsonlogger.JsonFormatter(log_format)

        file_handler.setFormatter(formatter)
        stdout_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)

    return logger
