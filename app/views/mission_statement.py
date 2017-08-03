from flask import render_template, g, redirect, url_for
from flask_login import current_user

from app.main import main
from app.forms import HomepageSearch


@main.route("/mission-statement", methods=['GET', 'POST'])
def mission_statement():

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

    return render_template("mission_statement.html", server_data=template_payload)
