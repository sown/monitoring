"""Icinga API interaction code."""
import difflib
import logging
import time

import requests

from .config import ICINGA_CA, ICINGA_PASS, ICINGA_URL, ICINGA_USER

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

    def _post_config(self, files) -> None:
        """Post the config to Icinga."""
        r = self._post(
            endpoint="config/stages/sown",
            data={
                "files": files,
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

    def _get_file(self, stage, filename):
        return self._get(
            endpoint=f"config/files/sown/{stage}/{filename}",
            accept="application/octet-stream",
        ).text

    def update_config(self, *, files) -> None:
        """Update the config and check that it worked."""
        self._post_config(files)

        self._wait_reload()

        if self._status() != "0":
            raise IcingaReloadFailedException()

    @property
    def current_stage(self):
        """Get the name of the current stage."""
        packages = self._get(
            endpoint="config/packages",
        ).json()["results"]
        package = [package for package in packages if package["name"] == "sown"]
        if not package:
            return False
        else:
            return package[0]["active-stage"]

    def get_current_files(self):
        """Get the files from the current stage."""
        stage = self.current_stage
        icingafiles = self._get(
            endpoint=f"config/stages/sown/{stage}",
        ).json()["results"]
        filenames = [file["name"] for file in icingafiles if file["type"] == "file"]

        files = {}
        for filename in filenames:
            files[filename] = self._get_file(stage, filename)
        return files

    def get_diff(self, files_new):
        """Geet a diff between the running configuration and a set of files."""
        files_old = self.get_current_files()
        filenames = set(files_new.keys()) | set(files_old.keys())
        icinga_internal_names = {"startup.log", "status", "include.conf"}
        diffs = []
        for filename in filenames - icinga_internal_names:
            new = files_new.get(filename, "").split("\n")
            old = files_old.get(filename, "").split("\n")
            diffs = diffs + list(difflib.unified_diff(old, new,
                                 fromfile=f"old/{filename}", tofile=f"new/{filename}",
                                 lineterm=""))
        if diffs:
            return "\n".join(diffs)
        else:
            return ""

    def log(self) -> None:
        """Get the Icinga log."""
        return self._get(
            endpoint=(f"config/files/sown/{self.stage}/startup.log"),
            accept="application/octet-stream",
        ).text
