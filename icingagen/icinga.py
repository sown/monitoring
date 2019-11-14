import requests
import logging
import time

from .config import ICINGA_URL, ICINGA_USER, ICINGA_PASS, ICINGA_CA
from .logging import logger_setup

logger_setup(__name__)
LOGGER = logging.getLogger(__name__)

class IcingaReloadFailedException(Exception):
    pass

class Icinga:
    def __init__(self) -> None:
        self.stage = ""

    def _post(test, endpoint, data, accept="application/json") -> None:
        return requests.post(ICINGA_URL + endpoint, json=data, auth=(ICINGA_USER, ICINGA_PASS), verify=ICINGA_CA, headers={"Accept": accept})
    
    def _get(test, endpoint, accept="application/json") -> None:
        return requests.get(ICINGA_URL + endpoint, auth=(ICINGA_USER, ICINGA_PASS), verify=ICINGA_CA, headers={"Accept": accept})
    
    def _post_config(self, hosts) -> None:
        r = self._post(endpoint="config/stages/sown", data={"files": {"conf.d/hosts-sown.conf": hosts}})
        self.stage = r.json()["results"][0]["stage"]
    
    def _wait_reload(self) -> None:
        status = 404
        LOGGER.info("Waiting for icinga to validate config")
        while status == 404:
          status = self._get(endpoint=(f"config/files/sown/{self.stage}/startup.log"), accept="application/octet-stream").status_code
          LOGGER.info("Still waiting...")
          time.sleep(1)

    def _status(self) -> None:
        return self._get(endpoint=(f"config/files/sown/{self.stage}/status"), accept="application/octet-stream").text
        
    def update_config(self, *, hosts) -> None:
          self._post_config(hosts)

          self._wait_reload()

          if self._status() != "0":
                raise IcingaReloadFailedException()
    
    def log(self) -> None:
        return self._get(endpoint=(f"config/files/sown/{self.stage}/startup.log"), accept="application/octet-stream").text
