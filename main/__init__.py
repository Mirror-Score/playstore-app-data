from flask import Flask
from flask_caching import Cache
from main.config import AppConfig

__all__ = ("cache", "create_app")

cache = Cache()


def create_app(config_class: object = AppConfig) -> Flask:
    """Create app instance, register services and update config variables

    Args:
        config_class (object, optional): Config class for app. Defaults to AppConfig.

    Returns:
        Flask: flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize cache
    cache.init_app(app)

    # register app blueprints
    from main.scrapper import scrapper
    from main.deploy import deploy

    app.register_blueprint(scrapper)
    app.register_blueprint(deploy)

    return app
