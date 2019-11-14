"""Logger Setup."""
import logging
import sys


def logger_setup(name) -> None:
    """Setup the logger."""
    root = logging.getLogger(name)
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)
