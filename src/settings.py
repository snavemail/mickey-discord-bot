import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv('DISCORD_API_SECRET')

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG", 
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "console2": {
            "level": "WARNING", 
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file ": {
            "level": "INFO", 
            "class": "logging.fileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose"
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False
        },
    }
}