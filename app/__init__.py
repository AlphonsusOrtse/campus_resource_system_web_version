
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.extensions import db


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(connection, connection_record):
    if connection.__class__.__module__.startswith("sqlite3"):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


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
