import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

DEFAULT_LOG_DIR = "logs"

class KafkaLogger:

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:

        if name in cls._loggers:
            return cls._loggers[name]
        
        log_level_name = os.environ.get("KAFKA_LOG_LEVEL", DEFAULT_LOG_LEVEL)
        log_level = LOG_LEVELS.get(log_level_name, logging.INFO)
        
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        if not logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            
            formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            
            log_to_file = os.environ.get("KAFKA_LOG_TO_FILE", "false").lower() == "true"
            if log_to_file:
                log_dir = os.environ.get("KAFKA_LOG_DIR", DEFAULT_LOG_DIR)
                
                os.makedirs(log_dir, exist_ok=True)
                
                file_handler = RotatingFileHandler(
                    os.path.join(log_dir, f"{name}.log"),
                    maxBytes=10*1024*1024,  
                    backupCount=5
                )
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                
                logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        
        return logger

def get_logger(name: str) -> logging.Logger:
    return KafkaLogger.get_logger(name)