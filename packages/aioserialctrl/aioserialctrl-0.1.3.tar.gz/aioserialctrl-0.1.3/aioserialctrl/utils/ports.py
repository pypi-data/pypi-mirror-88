import re

import seriallib

class PortInfo:
    def __init__(self, port, physical_name, friend_name, enum_name):
        self.port = port
        self.physical_name = physical_name
        self.friend_name = friend_name
        self.enum_name = enum_name

    def __str__(self):
        return f"{self.port}: {self.friend_name}"

def get_all():
    port_list = []
    for port, physical_name, friend_name, enum_name in seriallib.get_all_serial_port_info():
        port_list.append(
            PortInfo(
                port.decode("DBCS", errors="ignore"),
                physical_name.decode("DBCS", errors="ignore"),
                friend_name.decode("DBCS", errors="ignore"),
                enum_name.decode("DBCS", errors="ignore")
            )
        )

    return port_list

def grep(regexp):
    r = re.compile(regexp, re.I)
    for info in get_all():
        if r.search(info.port) or r.search(info.physical_name) or r.search(info.friend_name):
            yield info