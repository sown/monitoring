"""Render Icinga2 config."""
import logging
import sys

import jinja2

from .config import CONFIG_PATH

def render(*, devices, vms):
    jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
    template = jinjaEnv.get_template(CONFIG_PATH)

    print(template.render(devices=devices, vms=vms))
