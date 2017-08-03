from flask import redirect, url_for
from flask_login import logout_user, login_required

from app.main import main


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
