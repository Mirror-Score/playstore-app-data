from google_play_scraper import app


def get_data(id: str, keys=None):
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
    data = app(id, lang="en", country="in")  # defaults to 'en'  # defaults to 'us'

    data["current_version"] = data.get("version")

    if keys is not None:
        keys = keys.split(",")
        new_data = {}
        for key in keys:
            new_data[key] = data.get(key)
        data = new_data

    return data
