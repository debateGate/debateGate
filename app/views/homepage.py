from math import ceil

from flask import render_template, g, redirect, url_for
from flask_login import current_user

from app.main import main
from app.lib.queries import search_debates
from app.models import Debate
from app.forms import HomepageSearch

with_params = False

def homepage_with_params(searchtype="in-progress", terms="", page=1):

    global with_params

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
                                    page=1 ))

    if terms != "":
        debates, maxlen = search_debates(searchtype=searchtype, terms=terms, page=page, isGlobalSearch=True)
    else:
        debates, maxlen = search_debates(searchtype=searchtype, terms=terms, page=page)

    template_payload = {
        "debates": debates
    }

    template_payload["search_debates_form_multipage"] = search_debates_form

    if current_user.is_authenticated and current_user is not None:
        template_payload["user"] = g.user
        template_payload["is_vip"] = current_user.isVIP
    else:
        template_payload["auth_url"] = g.auth_url

    template_payload["pagenum"] = page
    template_payload["max_pagenum"] = maxlen
    template_payload["with_params"] = with_params
    template_payload["searchtype"] = searchtype

    if terms == "":
        template_payload["terms"] = "___blank___"
    else:
        template_payload["terms"] = terms

    return render_template("home.html", server_data=template_payload)


@main.route("/", methods=['GET', 'POST'])
def homepage():
    return homepage_with_params()

@main.route("/debates-<searchtype>/<terms>/<int:page>", methods=['GET', 'POST'])
def homepage_with_params_wrapper(searchtype="in-progress", terms="", page=1):
    global with_params
    with_params = True
    return homepage_with_params(searchtype, terms, page)
