from math import ceil

from flask import render_template, g, redirect, url_for
from flask_login import login_required

from app.main import main
from app.lib.queries import search_debates
from app.forms import HomepageSearch


@main.route("/search/debates-<searchtype>/<terms>/<int:page>", methods=['GET', 'POST'])
@login_required
def search(searchtype, terms, page=1):

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

    debates, maxlen = search_debates(searchtype=searchtype, terms=terms, page=page)

    template_payload = {
        "debates": debates,
        "user": g.user,
        "pagenum": page,
        "max_pagenum": maxlen,
        "searchtype": searchtype,
        "terms": terms
    }
    template_payload["search_debates_form_multipage"] = search_debates_form

    return render_template("search.html", server_data=template_payload) 
