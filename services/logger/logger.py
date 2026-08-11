import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "app.log"


def setup_logger():
    """
    Configure and return the main application logger.
    This function should be called once when the application starts.
    """

    # Create logs folder if it does not exist
    LOG_DIR.mkdir(exist_ok=True)

    # Create/get logger
    logger = logging.getLogger("app")

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Minimum level to save
    logger.setLevel(logging.INFO)

    # Log message format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,   # 5 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    formatter = logging.Formatter(
        "%(levelname)s | %(module)s:%(lineno)d | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    return logger