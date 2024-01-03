
from datetime import datetime
from typing import List
from models.station import Station

from models.tag import Tag


def get_stop_value(station: dict):
    tags = station['tags']
    for tag in tags:
        if tag['name'] == "M_Stop" and tag.value == False:
            return False
    return True

def create_stop_tag():
    info = {"name": "M_STOP",
            "datetime": datetime.now(),
            "tipo": "bool",
            "value": True}
    return Tag(**info)