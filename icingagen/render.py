"""Render Icinga2 config."""
import logging
import sys

import jinja2

def render(devices):
    jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
    template = jinjaEnv.get_template("config.j2")

    print(template.render(devices=devices))
