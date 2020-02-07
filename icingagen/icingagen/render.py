"""Render Icinga2 config."""
import jinja2


def render(*, devices, vms, template, racks):
    """Render a new Icinga configuration from jinja2 template and netbox objects."""
    jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="/"))
    template = jinjaEnv.get_template(template)

    return template.render(devices=devices, vms=vms, racks=racks)
