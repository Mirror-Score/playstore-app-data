import os


class AppConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "b4dcc56fb0826dfade3584d1ca2a682a")

    # cache configs
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60 * 60  # 1 hour

    # playstore url
    PLAYSTORE_URL = "https://play.google.com/store/apps/details"

    # Github api url
    GITHUB_URL = "https://api.github.com/meta"
