from bs4 import BeautifulSoup
import requests

BASE_URL = "https://play.google.com/store/apps/details"


def fetch_playstore(id: str, base_url=BASE_URL) -> str:
    """
    Fetch html from playstore with corresponding package id
    Args:
        id : Package id
        base_url(str): Base url of playstore
    Return:
        HTML document string
    """
    url = base_url + f"?id={id}"
    try:
        res = requests.get(url)
        return res.text
    except Exception as e:
        # TODO: implement log traceback to stderr
        print(e)
        return ""


def get_data(id: str):
    """
    Get app data of id passed from playstore
    Args:
        id: id of package to fetch from playstore

    Return:
        A dict of data associated with package id passed

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
    print("hello")
    data = {}
    html_doc = fetch_playstore(id)
    soup = BeautifulSoup(html_doc, "html.parser")

    for divs in soup.select(".hAyfc")[:5]:
        _key, _val = list(divs.children)
        key = "_".join(_key.text.lower().split(" "))
        val = str(_val.text).strip()
        data.update({key: val})

    return data
