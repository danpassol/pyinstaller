# test_logger.py

from core.logger import setup_logger

# Set verbose=True to see DEBUG logs
log = setup_logger(verbose=True)

def main():
    log.debug("This is a debug message (only visible in verbose mode).")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("Oops! Something went wrong.")

if __name__ == "__main__":
    main()
