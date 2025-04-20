# core/logger.py

import logging
from rich.logging import RichHandler

def setup_logger(verbose: bool = False):
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)]
    )
    return logging.getLogger("installer")

# Usage:
# from core.logger import setup_logger
# log = setup_logger(verbose=True)
# log.info("Hello!")
