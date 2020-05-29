"""Main file for config generator."""
import logging
import os

import click
from pynetbox.api import Api

from .config import CONFIG_DIR, NETBOX_URL
from .icinga import Icinga, IcingaReloadFailedException
from .logconfig import logger_setup
from .render import render

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Generate configuration and display diff but don't apply",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Only output configuration changes or errors",
)
def cli(dry_run: bool, quiet: bool):
    """Generate a new Icinga configuration."""
    logger_setup(quiet)

    nb = Api(NETBOX_URL, ssl_verify=False)
    icinga = Icinga()

    LOGGER.info("Building configuration from netbox")

    config = {}

    devices = nb.dcim.devices.filter(status="active")
    vms = nb.virtualization.virtual_machines.filter(status="active")
    racks = nb.dcim.racks.all()

    for vm in vms:
        vm.ips = nb.ipam.ip_addresses.filter(virtual_machine_id=vm.id)

    for device in devices:
        device.power_count = len(nb.dcim.power_ports.filter(device_id=device.id))
        device.ips = nb.ipam.ip_addresses.filter(device_id=device.id)

    for root, _, files in os.walk(CONFIG_DIR):
        for name in files:
            if name.endswith(".conf"):
                path = f"{root}/{name}"
                relative = os.path.relpath(f"{root}/{name}", CONFIG_DIR)
                LOGGER.debug(f"Found config file {path}")
                if ".j2." in name:
                    config[relative] = render(
                        devices=devices,
                        vms=vms,
                        racks=racks,
                        template=path,
                    )
                else:
                    with open(path, "r") as file:
                        config[relative] = file.read()

    diff = icinga.get_diff(config)
    if diff:
        LOGGER.warning(f"Changes:\n{diff}")
        if not dry_run:
            try:
                icinga.update_config(files=config)
                LOGGER.info("Icinga reloaded ok")
            except IcingaReloadFailedException:
                LOGGER.error("Icinga reload failed")
                LOGGER.error("Icinga logs:\n" + icinga.log())
    else:
        LOGGER.info("No change to config")
