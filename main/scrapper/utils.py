import traceback

import requests
from bs4 import BeautifulSoup
from flask import current_app


def fetch_playstore(id: str, base_url=None) -> str:
    """
    Fetch html from playstore with corresponding package id

    Args:
        id (str): Package id
        base_url (str, BASE_URL): Base url of playstore

    Returns:
        str: HTML document string
    """
    if base_url is None:
        base_url = current_app.config["PLAYSTORE_URL"]

    url = base_url + f"?id={id}"
    try:
        res = requests.get(url)
        return res.text
    except Exception:
        traceback.print_exc()
        return ""


def get_data(id: str):
    """
    Get app data of id passed from playstore
    Args:
        id (str): id of package to fetch from playstore

    Return:
        dict: A dict of data associated with package id passed

        example:

        {
            'Updated': 'October 12, 2021',
            'Size': '34M',
            'Installs': '10,000+',
            'Current_Version': '2.2.8',
            'Requires_Android': '5.0 and up'
        }

    Usage:
    >>> get_data("com.app.mirrorscore")
    {
        'updated': 'October 12, 2021',
        'size': '34M',
        'installs': '10,000+',
        'current_version': '2.2.8',
        'requires_android': '5.0 and up'
    }
    """
    data = {}
    html_doc = fetch_playstore(id)
    soup = BeautifulSoup(html_doc, "html.parser")

    for divs in soup.select(".hAyfc")[:5]:
        _key, _val = list(divs.children)
        key = "_".join(_key.text.lower().split(" "))
        val = str(_val.text).strip()
        data.update({key: val})

    return data
