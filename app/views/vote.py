from flask import render_template, g, session, redirect, url_for
from flask_login import current_user

from app.main import main, db
from app.lib.db_exec import add_user_to_votelist
from app.models import Debate, User


@main.route("/vote/<user_id>%<debate_id>%<pro_or_con>")
def vote(user_id, debate_id, pro_or_con):

    debate = Debate.query.filter_by(id=debate_id).first()

    if current_user.is_authenticated and current_user is not None:
        if (str(current_user.id) == user_id) and (session["voting_status"] is not None) and\
                (session["voting_status"]["canVote"]) and (session["voting_status"]["debate_id"] == debate_id) and\
                (debate.stage == "voting"):
            user_voted = User.query.filter_by(id=user_id).first()

            if pro_or_con == "pro":
                debate.pro_votes += 1
            elif pro_or_con == "con":
                debate.con_votes += 1
            db.session.commit()

            add_user_to_votelist(debate, user_voted)

            session["voting_status"]["canVote"] = False

            return redirect(url_for("debate_synopsis", debate_id=debate_id))

        else:
            pass

    return redirect(url_for("homepage"))
