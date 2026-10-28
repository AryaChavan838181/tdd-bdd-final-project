"""Flask application setup."""
import os
from flask import Flask
from service.models import db

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "local-project-development-only"),
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI", "sqlite:///catalogue.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db.init_app(app)

from service import routes  # noqa: E402,F401  -- register Flask handlers

with app.app_context():
    db.create_all()
