import logging
import os

class Logger:
    def __init__(self, log_file: str):
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    def info(self, message: str):
        logging.info(message)

    def error(self, message: str):
        logging.error(message)