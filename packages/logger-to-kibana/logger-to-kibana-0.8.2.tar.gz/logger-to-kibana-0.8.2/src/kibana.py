"""
This function handles the generation of the kibana visualization
"""
from src.configuration import config

import requests
import copy
from src.utils import visualization
from src.utils import dashboard
from src.aws_credentials import aws_auth
from itertools import groupby
from multiprocessing import Pool as ThreadPool


def generate_and_send_visualizations(folder_name: str, items: []):
    grouped_items = group_items(items)
    if grouped_items:
        title_vis = []
        for group in grouped_items:
            title = get_title_from_group(folder_name, group[0])
            vis = copy.copy(generate_folder_visualization(title, group))
            title_vis.append({
                "title": title,
                "vis": vis
            })
        generated_ids = send_visualization_pool(title_vis)

        generated_dashboard = dashboard.generate_dashboard(folder_name,
                                                           generated_ids)
        send_dashboard(folder_name, generated_dashboard)


def get_title_from_group(folder_name: str, group: dict) -> str:
    return (f"{folder_name} {group['subfolder']} "
            f"{group['filename']} {group['function']}")


def generate_folder_visualizations(folder_name: str, items: []) -> []:
    result = []
    grouped_items = group_items(items)
    if grouped_items:
        for group in grouped_items:
            title = get_title_from_group(folder_name, group[0])
            result.append(generate_folder_visualization(title, group))
    return result


def group_items(items: []) -> []:
    groups = []
    sorted_reader = sorted(items, key=lambda d:
                           (d['subfolder'], d['filename'], d['function']))
    for k, g in groupby(sorted_reader, key=lambda d:
                        (d['subfolder'], d['filename'], d['function'])):
        groups.append(list(g))
    return groups


def generate_folder_visualization(folder_name: str, items: []) -> dict:
    return visualization.generate_visualization(folder_name, items)


def send_visualization_pool(title_vis: dict) -> []:
    pool = ThreadPool(100)
    generated_ids = pool.map(send_visualization, title_vis)
    pool.close()
    pool.join()
    return generated_ids


def send_visualization(attributes: dict) -> str:
    headers = {"kbn-xsrf": "true"}
    data = {"attributes": attributes["vis"]}
    generated_id = f"generated-{attributes['title']}"
    url = (
        f"""{config.kibana.BaseUrl}/api/saved_objects/visualization/"""
        f"""{generated_id}?overwrite=true"""
    )
    auth = aws_auth() if (config.kibana.AuthType == "aws") else None

    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=auth,
    )

    print('send_visualization response:', response.text)

    return generated_id


def send_dashboard(folder_name: str, attributes: dict):
    headers = {"kbn-xsrf": "true"}
    data = {"attributes": attributes}
    url = (
        f"""{config.kibana.BaseUrl}/api/saved_objects/dashboard/"""
        f"""generated-{folder_name}?overwrite=true"""
    )
    auth = aws_auth() if (config.kibana.AuthType == "aws") else None

    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=auth,
    )

    print('send_dashboard response:', response.text)
