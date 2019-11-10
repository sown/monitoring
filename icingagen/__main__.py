"""Main file for config generator."""
from pynetbox.api import Api 

from icingagen import render, NETBOX_URL

nb = Api(NETBOX_URL, ssl_verify=False)

render(
  devices=nb.dcim.devices.all(),
  vms=nb.virtualization.virtual_machines.all(),
)
