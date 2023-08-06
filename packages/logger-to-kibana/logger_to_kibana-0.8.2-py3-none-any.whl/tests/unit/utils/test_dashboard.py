from src.utils import dashboard
from pytest import mark, raises
from unittest.mock import patch
from tests import helpers


@mark.parametrize(
    "path_name, items, expected",
    [
        ("Valid", [],
         "dashboard_with_valid_values.json"),
        ("/", [],
         "dashboard_empty.json")
    ]
)
def test_generate_dashboard_integration(path_name, items, expected):
    assert helpers.get_test_results_json_file(expected) == \
        dashboard.generate_dashboard(path_name, items)


@patch.object(dashboard, "generate_panels_json")
@patch.object(dashboard, "set_title")
def test_generate_dashboard(set_title, generate_panels_json):
    dashboard.generate_dashboard("path", [])
    assert set_title.call_count == 1
    assert generate_panels_json.call_count == 1


def test_set_title_value_error():
    with raises(ValueError):
        dashboard.set_title(None)


@mark.parametrize(
    "path_name, expected",
    [
        ("Secret", "[Generated] - Secret"),
        ("fdsafd", "[Generated] - fdsafd")
    ]
)
def test_set_title(path_name, expected):
    dashboard.set_title(path_name)
    assert dashboard.dashboard['title'] == expected


@patch.object(dashboard, "generate_panel_for_item")
@mark.parametrize(
    "items, call_count",
    [
        ([], 0),
        (['one'], 1),
        (['one', 'two'], 2),
        (['one', 'two', 'three'], 3),
    ]
)
def test_generate_panels_json(generate_panel_for_item,
                              items, call_count):
    generate_panel_for_item.return_value = {}
    dashboard.generate_panels_json(items)
    assert call_count == generate_panel_for_item.call_count


@mark.parametrize(
    "panel_index, y, iden",
    [
        (None, None, None),
        ("1", None, None),
        (None, 1, None),
        (None, None, "valid"),
        ("1", 1, None),
        (None, 1, "valid"),
        ("1", None, "valid"),
    ]
)
def test_generate_panel_for_item_value_error(panel_index, y, iden):
    with raises(ValueError):
        dashboard.generate_panel_for_item(panel_index, y, iden)


@mark.parametrize(
    "panel_index, y, iden, expected",
    [
        ("1", 2, "valid", {
            "panelIndex": "1",
            "gridData": {
                "y": 2,
                "i": "1"
            },
            "id": "valid",
        }),
        ("123", 456, "Something more substancial", {
            "panelIndex": "123",
            "gridData": {
                "y": 456,
                "i": "123"
            },
            "id": "Something more substancial",
        }),
    ]
)
def test_generate_panel_for_item_valid(panel_index, y, iden,
                                       expected):
    result = dashboard.generate_panel_for_item(panel_index, y, iden)
    assert result["panelIndex"] == expected["panelIndex"]
    assert result["gridData"]["y"] == expected["gridData"]["y"]
    assert result["gridData"]["i"] == expected["gridData"]["i"]
    assert result["id"] == expected["id"]

