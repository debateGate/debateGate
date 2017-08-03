from math import ceil

from flask import render_template, g, redirect, url_for
from flask_login import current_user

from app.lib.utilities import paginate_list

from app.main import main
from app.models import User, Debate
from app.lib.queries import find_user_debate_stance
from app.forms import HomepageSearch


@main.route("/profile/<int:user_id>/<int:page>", methods=['GET', 'POST'])
def profile(user_id, page=1):

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

    profile_user = User.query.filter_by(id=user_id).first()

    debates = []

    for debate in Debate.query.all():
        for relation in debate.users:
            if relation.user == profile_user:
                user_pro, user_con = find_user_debate_stance(debate)

                i = {
                     "id": debate.id,
                     "user_pro": user_pro,
                     "topic": debate.topic,
                     "max_round_number": debate.max_round_number,
                     "current_round_number": debate.current_round_number,
                     "user_con": user_con,
                     "is_timed": debate.isTimed,
                     "stage": debate.stage,
                     "views": debate.views
                }

                debates.append(i)
                break

    if profile_user is not None:
        prof_user = {
            "name": profile_user.name,
            "avatar": profile_user.avatar,
            "wins": profile_user.wins,
            "losses": profile_user.losses
        }
    else:
        return("No user id, " + user_id)

    if current_user.is_authenticated and current_user is not None:
        template_payload["user"] = g.user
    else:
        template_payload["auth_url"] = g.auth_url

    debates = list(paginate_list(debates, main.config["POSTS_PER_PAGE"]))

    template_payload["max_pagenum"] = ceil(len(debates))

    try:
        debates = debates[page - 1]
    except IndexError:
        debates = []

    template_payload["prof_user"] = prof_user
    template_payload["debates"] = debates
    template_payload["pagenum"] = page
    template_payload["user_id"] = user_id

    return render_template("profile.html", server_data=template_payload)
