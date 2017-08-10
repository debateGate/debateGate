"""
This file contains the logic to start the application, but should never be
run directly -- wsgi.py exists in the base directory for that purpose in development,
and the app server should handle it in production via run.sh
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

main = Flask(__name__)
main.config.from_object(config["dev"]) # change to dev for devving

db = SQLAlchemy(main)
migrate = Migrate(main, db)

login_manager = LoginManager(main)
login_manager.session_protection = "strong"
login_manager.login_view = "homepage"

# import models, views, and libs down here to avoid circular imports when these files need db
# and main objects

from app.models import User

from app.lib.pre_post_execution_funcs import get_user_login_data, add_header

from app.views import create_or_join_debate, debate_synopsis, gCallBack,\
homepage, logout, mission_statement, claims, profile, search, vote, privacy_statement,\
settings
from app.views.error_handlers import page_not_found, something_horrible_happened
from app.views.api import check_if_debate_stage_has_advanced


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()
