import json
from flask import session, redirect, url_for, request
from flask_login import login_user, current_user

from requests.exceptions import HTTPError

from config import Auth
from app.main import main, db
from app.lib.utilities import send_email
from app.lib.auth import get_google_auth
from app.models import User

from app.lib.email_strings import generate_greetings_email

@main.route("/gCallBack")
def gCallBack():

    # deals with all the situations in which we don't want to try to log in the
    # user
    if current_user.is_authenticated and current_user is not None:
        return redirect(url_for('homepage'))

    if "error" in request.args:
        if request.args.get("error") == "access_denied":
            return redirect(url_for("homepage"))
        return "Error encountered."

    if "code" not in request.args and "state" not in request.args:
        return redirect(url_for("homepage"))

    # Execution gets to this point once we are certain we want to authenticate
    # and/or store the user.

    # Get previously saved state
    google = get_google_auth(state=session["oauth_state"])

    # If there is no error, use the blank state to request a token from the
    # token uri, using our secret. This is only allowed if the request.url
    # confirms that the user has allowed us to do so.
    try:
        token = google.fetch_token(Auth.TOKEN_URI,
                                   client_secret=Auth.CLIENT_SECRET,
                                   authorization_response=request.url)
    except HTTPError:
        return "HTTPError occurred."

    # Initialize our final state with the requested auth token and use it to
    # get access to user data.
    google = get_google_auth(token=token)
    resp = google.get(Auth.USER_INFO)

    # if the request returns with no errors
    if resp.status_code == 200:

        # Get all the user data we need. If the user doesn't exist, create it.
        user_data = resp.json()
        email = user_data["email"]
        user = User.query.filter_by(email=email).first()

        new_user = False
        if user is None:
            user = User()
            user.email = email
            user.wins = 0
            user.losses = 0
            new_user = True

        if user.sync_with_google == True:
            user.name = user_data["name"]
        user.tokens = json.dumps(token)
        user.avatar = user_data["picture"]

        db.session.add(user)
        db.session.commit()

        if new_user == True:
            send_email(
                generate_greetings_email(),
                user.email)

        login_user(user)

    return redirect(url_for("homepage"))

    return "Could not fetch your information."
