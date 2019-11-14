"""Icinga API interaction code."""
import logging
import time

import requests

from .config import ICINGA_CA, ICINGA_PASS, ICINGA_URL, ICINGA_USER
from .logging import logger_setup

logger_setup(__name__)
LOGGER = logging.getLogger(__name__)


class IcingaReloadFailedException(Exception):
    """Icinga failed to reload."""

    pass


class Icinga:
    """Icinga connection and control."""

    def __init__(self) -> None:
        self.stage = ""

    def _post(test, endpoint, data, accept="application/json") -> None:
        """Send a post request to the Icinga API."""
        return requests.post(
            ICINGA_URL + endpoint,
            json=data,
            auth=(ICINGA_USER, ICINGA_PASS),
            verify=ICINGA_CA,
            headers={"Accept": accept},
        )

    def _get(test, endpoint, accept="application/json") -> None:
        """Send a GET request to the Icinga API."""
        return requests.get(
            ICINGA_URL + endpoint,
            auth=(ICINGA_USER, ICINGA_PASS),
            verify=ICINGA_CA,
            headers={"Accept": accept},
        )

    def _post_config(self, hosts) -> None:
        """Post the config to Icinga."""
        r = self._post(
            endpoint="config/stages/sown",
            data={
                "files": {
                    "conf.d/hosts-sown.conf": hosts,
                },
            },
        )
        self.stage = r.json()["results"][0]["stage"]

    def _wait_reload(self) -> None:
        """Wait for Icinga to reload."""
        status = 404
        LOGGER.info("Waiting for icinga to validate config")
        while status == 404:
            status = self._get(
                endpoint=(f"config/files/sown/{self.stage}/startup.log"),
                accept="application/octet-stream",
            ).status_code
            LOGGER.info("Still waiting...")
            time.sleep(1)

    def _status(self):
        """Get the Icinga status of a new stage."""
        return self._get(
            endpoint=(f"config/files/sown/{self.stage}/status"),
            accept="application/octet-stream",
        ).text

    def update_config(self, *, hosts) -> None:
        """Update the config and check that it worked."""
        self._post_config(hosts)

        self._wait_reload()

        if self._status() != "0":
            raise IcingaReloadFailedException()

    def log(self) -> None:
        """Get the Icinga log."""
        return self._get(
            endpoint=(f"config/files/sown/{self.stage}/startup.log"),
            accept="application/octet-stream",
        ).text
