#!/usr/bin/python3

"""
Display human friendly description of some UPnP service

Usage:

  ./upnp-display-intrfaces $URI

where $URI is the URI found in the SSDP message (`LOCATION` header).
"""

import requests
import sys
import lxml.etree
from urllib.parse import urljoin

UPNP_DEV_NS = "urn:schemas-upnp-org:device-1-0"
UPNP_SERV_NS = "urn:schemas-upnp-org:service-1-0"
NS = {"dev": UPNP_DEV_NS, "serv": UPNP_SERV_NS}


def get_xml(uri):
    response = requests.get(uri)
    response.raise_for_status()
    return lxml.etree.XML(response.content)


def dump_interface(type, uri):

    print(f"interface {type} {{")

    description = get_xml(uri)
    action_list = description.find("serv:actionList", namespaces=NS)
    for action in action_list.findall("serv:action", namespaces=NS):

        name = action.find("serv:name", namespaces=NS).text

        argument_list = action.find("serv:argumentList", namespaces=NS)

        if argument_list is None:
            arguments = []
            outputs = []
        else:
            arguments = [
                argument.find("serv:name", namespaces=NS).text
                for argument in argument_list.findall("serv:argument", namespaces=NS)
                if argument.find("serv:direction", namespaces=NS).text == "in"
            ]

            outputs = [
                argument.find("serv:name", namespaces=NS).text
                for argument in argument_list.findall("serv:argument", namespaces=NS)
                if argument.find("serv:direction", namespaces=NS).text == "out"
            ]

        print(f"  {name}({', '.join(arguments)}) -> ({', '.join(outputs)})")

    print("}")


uri = sys.argv[1]
doc = get_xml(uri)
for service in doc.xpath("//dev:service", namespaces=NS):
    service_type = service.find("dev:serviceType", namespaces=NS).text
    service_id = service.find("dev:serviceId", namespaces=NS).text
    scdp_url = urljoin(uri, service.find("dev:SCPDURL", namespaces=NS).text)
    control_url = urljoin(uri, service.find("dev:controlURL", namespaces=NS).text)
    event_url = urljoin(uri, service.find("dev:eventSubURL", namespaces=NS).text)
    dump_interface(service_type, scdp_url)
