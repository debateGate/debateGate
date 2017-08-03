from flask import render_template, g, redirect, url_for
from flask_login import login_required, current_user

from app.main import main
from app.models import Debate, User
from app.forms import DebateCreate, DebateSearchBar

from app.lib.db_exec import add_user_to_debate
from app.forms import HomepageSearch


@main.route("/create-or-join-debate", methods=['GET', 'POST'])
@login_required
def create_or_join_debate():

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

        create_debate_form = DebateCreate(prefix="create_debate_form")
        search_debates_form_bottom = DebateSearchBar(prefix="search_debate_form")

        template_payload = {
                "user": g.user,
                "create_debate_form": create_debate_form,
                "search_debates_form": search_debates_form
        }

        template_payload["search_debates_form_multipage"] = search_debates_form

        if create_debate_form.validate_on_submit():

            debate = Debate()
            debate.dtype = create_debate_form.debate_type.data
            debate.topic = create_debate_form.topic.data
            debate.max_round_number = create_debate_form.max_round_number.data
            debate.max_claim_number = 1 #create_debate_form.max_claim_number.data
            debate.isTimed = create_debate_form.is_timed.data
            debate.current_round_number = 1
            debate.views = 0
            debate.stage = "pro"

            user = User.query.filter_by(id=current_user.id).first()
            user_type = create_debate_form.pro_or_con.data

            add_user_to_debate(debate, user, user_type=user_type)

            return redirect(url_for("debate_synopsis", debate_id=debate.id))

        if search_debates_form_bottom.validate_on_submit():
            return redirect(url_for("search",
                                    searchtype="joinable",
                                    terms=search_debates_form.search_bar.data,
                                    page=1
            ))

        return render_template("create_or_join_debate.html", server_data=template_payload) 
