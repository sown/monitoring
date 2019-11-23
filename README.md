This is SOWN's monitoring configuration management. It builds an Icinga2 configuration from templates, using data from Netbox, and submits the generated configuration to Icinga2's API.

## Working on the Icinga configuration
Icinga2 runs on monitor2, with this repo checked out at /opt/sown/monitoring. You can work on the Icinga config like follows:
```console
$ ssh monitor2
root@monitor2:~# cd /opt/sown/monitoring/config
root@monitor2:/opt/sown/monitoring/config# # hack hack hack
```
When done:
```console
root@monitor2:~# icingagen
2019-11-23 03:11:33,638 - INFO - icingagen.__main__ - Building configuration from netbox
...
2019-11-23 03:11:52,864 - INFO - icingagen.__main__ - Icinga reloaded ok
```
If Icinga rejects the new configuration, the script will let you know and print out the error output from icinga's log.

Please remember to commit + push your changes when done :)

Parts of Icinga's configuration also still live in the standard system directory at `/etc/icinga2/`. These should be moved to our configuration management where possible, but to reload changes there you can `systemctl reload icinga2` and `journalctl -eu icinga2` to read the log.

## Viewing the generated Icinga configuration
The generated configuration is sent to Icinga over its API, as the sown package.
You'll find the generated configurations at `/var/lib/icinga2/api/packages/sown`, with a directory for each generated configuration. The current stage id can be found in `activate-stage` in that directory.

The following can be helpful to quickly go to that directory, where you'll find the running configuration:
```console
root@monitor2:~# cd /var/lib/icinga2/api/packages/sown/$(cat /var/lib/icinga2/api/packages/sown/active-stage)
root@monitor2:/var/lib/icinga2/api/packages/sown/02302d4e-2f57-44e9-9564-8102d7b4b8e6# ls
conf.d  include.conf  startup.log  status  zones.d
```

If the configuration fails to reload, Icinga will also print out the full path then.

You can also dump objects built from the configuration and view them like:
```console
root@monitor2:~# icinga2 object list | less
```

## Working on the codebase
The python module is installed in a virtualenv at `/opt/sown/monitoring/venv`, in "editable" mode, so the installed package is simply symlinks to the source. Therefore, you can happily work on the source code in place at `/opt/sown/monitoring/icingagen/icingagen/`.

The `icingagen` CLI command runs the main function that you'll find in `__main__.py`.

To add any dependencies, edit setup.py, and reinstall it like follows:
```console
root@monitor2:/opt/sown/monitoring/icingagen# ../venv/bin/pip3 install -e .[dev]
```

Also run the linter after making any changes, and ensure it completes without finding any issues:
```console
root@monitor2:/opt/sown/monitoring/icingagen# source ../venv/bin/activate
(venv) root@monitor2:/opt/sown/monitoring/icingagen# make lint
flake8 icingagen  
(venv) root@monitor2:/opt/sown/monitoring/icingagen# # we're all good!
```
