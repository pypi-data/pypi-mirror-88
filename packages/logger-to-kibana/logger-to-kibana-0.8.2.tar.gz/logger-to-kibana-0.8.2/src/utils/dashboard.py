"""
This module handles the Kibana dashboard generation
"""
import copy
import json
from src.configuration import config

dashboard = {"title": ""}
kibana_meta = {
    "searchSourceJSON": json.dumps(
        {
            "query": {"query": "", "language": "lucene"},
            "filter": [],
        }
    ),
}

panels_json = {
    "embeddableConfig": {},
    "gridData": {
      "x": 0,
      "y": 0,  # This will give some space
      "w": 48,
      "h": 9,
      "i": "1"
    },
    "id": "",
    "panelIndex": "",  # increase by one
    "type": "visualization",
    "version": config.kibana.Version
}


def generate_dashboard(title: str, items: []) -> dict:
    set_title(title)
    generate_panels_json(items)
    dashboard["kibanaSavedObjectMeta"] = kibana_meta

    return dashboard


def set_title(title: str):
    if not isinstance(title, str):
        raise ValueError("title should be a string")
    dashboard["title"] = "[Generated] - " + title


def generate_panels_json(items: []):
    json_panels = []
    for num, item in enumerate(items):
        json_panels.append(
            generate_panel_for_item(str(num), num*9, str(item)))
    dashboard["panelsJSON"] = json.dumps(json_panels)


def generate_panel_for_item(panel_index: int, y: int, identifier: str) -> dict:
    if not isinstance(panel_index, str):
        raise ValueError("panel_index should be a str")
    if not isinstance(y, int):
        raise ValueError("y should be a int")
    if not isinstance(identifier, str):
        raise ValueError("identifier should be a str")

    panels_json["panelIndex"] = panel_index
    panels_json["gridData"]["y"] = y
    panels_json["gridData"]["i"] = panel_index
    panels_json["id"] = str(identifier)

    return copy.deepcopy(panels_json)
