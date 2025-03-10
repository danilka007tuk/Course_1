import logging
import os
from logging import Logger


def get_logger(file_name: str, log_file: str) -> Logger:
    """Функция настройки логов для модулей"""
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file, mode="w+")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s -  %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
