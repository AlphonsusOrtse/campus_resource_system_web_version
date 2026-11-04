
from flask import Flask
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.update(
        SECRET_KEY="development-only-change-before-deployment",
        SQLALCHEMY_DATABASE_URI="sqlite:///campus.db",
    )

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    from app import models
    from app.routes import main
    app.register_blueprint(main)

    return app
