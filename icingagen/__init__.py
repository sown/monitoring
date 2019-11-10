"""Icinga Config Generator."""

from .logging import logger_setup
from .render import render

NETBOX_URL = "http://netbox.sown.org.uk"

__all__ = [
  "NETBOX_URL",
  "render",
]
