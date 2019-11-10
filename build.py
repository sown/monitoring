#!/usr/bin/python3
import requests
import jinja2

jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./"))
template = jinjaEnv.get_template("config.j2")

apiroot = "http://netbox.sown.org.uk/api/"
devices = requests.get(apiroot + "dcim/devices/").json()["results"]
print(template.render(devices=devices))
