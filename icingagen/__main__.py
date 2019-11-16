"""Main file for config generator."""
import logging
import os

from pynetbox.api import Api

from .config import CONFIG_DIR, NETBOX_URL
from .icinga import Icinga, IcingaReloadFailedException
from .logging import logger_setup
from .render import render


def main():
    """Entrypoint."""
    logger_setup(__name__)
    LOGGER = logging.getLogger(__name__)

    nb = Api(NETBOX_URL, ssl_verify=False)
    icinga = Icinga()

    LOGGER.info("Building configuration from netbox")

    config = {}

    devices = nb.dcim.devices.all()
    vms = nb.virtualization.virtual_machines.all()

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
                        ips=ips,
                        template=path,
                    )
                else:
                    with open(path, "r") as file:
                        config[relative] = file.read()

    try:
        icinga.update_config(files=config)
        LOGGER.info("Icinga reloaded ok")
    except IcingaReloadFailedException:
        LOGGER.error("Icinga reload failed")
        LOGGER.error("Icinga logs:\n" + icinga.log())


if __name__ == "__main__":
    main()
