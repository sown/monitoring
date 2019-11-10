"""Logger Setup."""
import logging
import sys


def logger_setup() -> None:
    """Setup the logger."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)
