import pytest
from src import kibana
from src.utils import dashboard
from unittest.mock import patch, Mock
from tests import helpers
import requests


@patch.object(dashboard, "generate_dashboard")
@patch.object(kibana, "group_items")
@patch.object(kibana, "get_title_from_group")
@patch.object(kibana, "generate_folder_visualization")
@patch.object(kibana, "send_dashboard")
@patch.object(kibana, "send_visualization_pool")
@pytest.mark.parametrize(
    "items_group, expected_calls",
    [
        (None, 0),
        ([], 0),
        ([[{'subfolder': 'bla', 'filename': 'file', 'function': None}]], 1)
    ]
)
def test_generate_and_send_visualizations(
        send_vis, send_dash, generate_vis, get_title,
        group_items, generate_dash,
        items_group, expected_calls):
    group_items.return_value = items_group
    kibana.generate_and_send_visualizations("test", [])
    assert group_items.call_count == 1
    assert get_title.call_count == expected_calls
    assert generate_vis.call_count == expected_calls
    assert generate_dash.call_count == expected_calls
    assert send_vis.call_count == expected_calls
    assert send_dash.call_count == expected_calls


@patch.object(kibana, "group_items")
@patch.object(kibana, "get_title_from_group")
@patch.object(kibana, "generate_folder_visualization")
@pytest.mark.parametrize(
    "items_group, expected_calls",
    [
        (None, 0),
        ([], 0),
        ([[{'subfolder': 'bla', 'filename': 'file', 'function': None}]], 1)
    ]
)
def test_generate_folder_visualizations(
        generate, get_title, group_items,
        items_group, expected_calls):
    group_items.return_value = items_group
    kibana.generate_folder_visualizations("test", [])
    assert group_items.call_count == 1
    assert get_title.call_count == expected_calls
    assert generate.call_count == expected_calls


@pytest.mark.parametrize(
    "folder_name, group, expected",
    [
        ("bla",
         {'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'},
         "bla ble bli blo"),
        ("folder",
         {'subfolder': 'sub', 'filename': 'file', 'function': 'func'},
         "folder sub file func"),
    ]
)
def test_get_title_from_group(folder_name, group, expected):
    assert kibana.get_title_from_group(folder_name, group) == expected



@pytest.mark.parametrize(
    "items, expected",
    [
        ([{'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'}],
         [[{'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'}]]
         ),
        ([{'subfolder': 'ble', 'filename': 'bla', 'function': 'blo'},
         {'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'},
         {'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'},
         {'subfolder': 'bli', 'filename': 'bli', 'function': 'blo'},
         {'subfolder': 'bli', 'filename': 'blo', 'function': 'blo'}],
         [[{'subfolder': 'ble', 'filename': 'bla', 'function': 'blo'}],
          [{'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'},
           {'subfolder': 'ble', 'filename': 'bli', 'function': 'blo'}],
          [{'subfolder': 'bli', 'filename': 'bli', 'function': 'blo'}],
          [{'subfolder': 'bli', 'filename': 'blo', 'function': 'blo'}]],
         )
    ]
)
def test_group_items(items, expected):
    assert expected == kibana.group_items(items)


@pytest.mark.parametrize(
    "path_name, items, expected",
    [
        ("/", [], "visualization_with_empty_vis_state.json"),
        ("Valid", [], "visualization_with_valid_values.json")
    ]
)
def test_generate_folder_visualization_integration(path_name, items, expected):
    kibana.config.kibana.VisualizationType = 'table'
    assert helpers.get_test_results_json_file(expected) == \
        kibana.generate_folder_visualization(path_name, items)


@patch.object(kibana.visualization, "generate_visualization")
def test_generate_folder_visualization(visualization):
    kibana.generate_folder_visualization("test", [])
    assert visualization.call_count == 1


@patch.object(kibana, "ThreadPool")
def test_send_visualization_pool(thread_pool):
    pool = Mock()
    thread_pool.return_value = pool
    title_vis = {
        "title": "my test title",
        "vis": {
            "something": "else"
        }
    }

    kibana.send_visualization_pool(title_vis)

    thread_pool.assert_called_once()
    pool.map.assert_called_once_with(kibana.send_visualization, title_vis)
    pool.close.assert_called_once()
    pool.join.assert_called_once()


@patch.object(kibana, "aws_auth")
@patch.object(kibana, "config")
@patch.object(requests, "post")
@pytest.mark.parametrize(
    "attributes, return_auth_type, aws_auth_calls",
    [
        ({"title": "path_name",
          "vis": []}, None, 0),
        ({"title": "path_name",
          "vis": []}, 'bla', 0),
    ]
)
def test_send_visualization(
        post, config, aws_auth, attributes,
        return_auth_type, aws_auth_calls):
    config.kibana.AuthType.return_value = return_auth_type
    kibana.send_visualization(attributes)
    assert aws_auth.call_count == aws_auth_calls
    assert post.call_count == 1


@patch.object(kibana, "aws_auth")
@patch.object(kibana, "config")
@patch.object(requests, "post")
@pytest.mark.parametrize(
    "path_name, items, return_auth_type, aws_auth_calls",
    [
        ("path_name", [], None, 0),
        ("path_name", [], 'bla', 0),
    ]
)
def test_send_dashboard(
        post, config, aws_auth, path_name,
        items, return_auth_type, aws_auth_calls):
    config.kibana.AuthType.return_value = return_auth_type
    kibana.send_dashboard(path_name, items)
    assert aws_auth.call_count == aws_auth_calls
    assert post.call_count == 1
