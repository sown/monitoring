"""Main file for config generator."""
import logging

from pynetbox.api import Api

from .config import NETBOX_URL
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

    config = render(
        devices=nb.dcim.devices.all(), vms=nb.virtualization.virtual_machines.all(),
    )

    try:
        icinga.update_config(hosts=config)
        LOGGER.info("Icinga reloaded ok")
    except IcingaReloadFailedException:
        LOGGER.error("Icinga reload failed")
        LOGGER.error("Icinga logs:\n" + icinga.log())


if __name__ == "__main__":
    main()
