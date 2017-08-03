from flask import render_template, g, redirect, url_for
from flask_login import current_user, login_required

from app.main import main, db
from app.models import User
from app.forms import HomepageSearch, EmailSettings


@main.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():

    search_debates_form = HomepageSearch(prefix="search_debate_form")

    if search_debates_form.validate_on_submit():
        if search_debates_form.search_bar.data == "":
            return redirect(url_for("homepage_with_params_wrapper",
                                    searchtype=search_debates_form.debate_type.data,
                                    terms="___blank___",
                                    page=1 ))
        else:
            return redirect(url_for("homepage_with_params_wrapper",
                                    searchtype=search_debates_form.debate_type.data,
                                    terms=search_debates_form.search_bar.data,
                                    page=1))

    template_payload = {}

    template_payload["search_debates_form_multipage"] = search_debates_form

    if current_user.is_authenticated and current_user is not None:
        template_payload["user"] = g.user
    else:
        template_payload["auth_url"] = g.auth_url

    user_settings = User.query.filter_by(id=current_user.id).first()
    settings_form = EmailSettings(obj=user_settings)

    template_payload["settings_form"] = settings_form

    if settings_form.validate_on_submit():
        user_settings.send_user_joined_emails = bool(settings_form.send_user_joined_emails.data)
        user_settings.send_round_continue_emails = bool(settings_form.send_round_continue_emails.data)
        user_settings.send_voting_notification_emails = bool(settings_form.send_voting_notification_emails.data)
        user_settings.send_debate_finished_emails = bool(settings_form.send_debate_finished_emails.data)
        db.session.commit()

    return render_template("settings.html", server_data=template_payload)
