"""
Contains all functions that should be executed before any request.

Note that the serving of static files would usually be handled by the app
server in production, precluding the possibility of bugs arising due to
@main.before_request decorated functions being called on the loading of said
static files. In development, however, that isn't a possibility, so there are
checks to make sure that these functions aren't called on static files, even
though it may seem redundant.
"""

import datetime
from flask import session, g, request
from flask_login import current_user

from app.main import main
from config import Auth
from app.lib.auth import get_google_auth
from app.models import User


@main.before_request
def get_user_login_data():
    """
    Gets the user object and creates a dict of what is necessary for _base.html's
    header image, login/logout buttons, etc, if the user is logged in. Otherwise, get
    the login link and set up the eternally cursed OAuth login system via session[].
    """

    session.permanent = True #31 day limit by default; if False, makes it expire on browser close

    # We don't want to run this for any view that doesn't have a template, nor
    # do we want to run this for static files.
    if request.endpoint not in ("gCallBack", "logout", "join_debate", "vote") and \
       "/static" not in request.path:

        if current_user.is_authenticated and current_user is not None:
            user_raw = User.query.filter_by(id=current_user.get_id()).first()
            g.user = {
                      "name": user_raw.name,
                      "avatar": user_raw.avatar
            }

        else:
            # Get empty OAuth2 state
            google = get_google_auth()

            # Get auth_url for user authentication and state for a blank state
            # to request tokens with
            auth_url, state = google.authorization_url(Auth.AUTH_URI,
                                                       access_type="online")
            session["oauth_state"] = state
            g.auth_url = auth_url


@main.after_request
def add_header(r):
    """
    Disable caching.
    """

    # We don't want to run this for any view that doesn't have a template, nor
    # do we want to run this for static files.
    if request.endpoint not in ("gCallBack", "logout", "join_debate", "vote") and \
       "/static" not in request.path:

        r.headers['Last-Modified'] = datetime.datetime.now()
        r.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        r.headers['Pragma'] = 'no-cache'
        r.headers['Expires'] = '-1'

    return r
