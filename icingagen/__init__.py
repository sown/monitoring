"""Icinga Config Generator."""

from .config import CONFIG_PATH, NETBOX_URL
from .logging import logger_setup
from .render import render

__all__ = [
  "NETBOX_URL",
  "CONFIG_PATH",
  "render",
]
