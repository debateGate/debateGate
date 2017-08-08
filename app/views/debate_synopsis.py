import datetime

from flask import render_template, g, redirect, url_for, session
from flask_login import current_user

from wtforms.validators import DataRequired, Length

from app.main import main, db
from app.models import Debate, User, Claim
from app.forms import ClaimSupport, JoinDebate

from app.lib.db_exec import add_user_to_debate
from app.lib.queries import return_rounds_of_debate, find_user_debate_stance

from app.lib.utilities import send_email
from app.lib.email_strings import generate_round_continue_email, generate_voting_session_email, \
    generate_debate_complete_email, generate_user_joined_debate_email, \
    generate_debate_complete_tied_email

from app.forms import HomepageSearch


def manage_debate_end_emails(debate, user_pro, user_con):
    if debate.stage == "finished" and debate.has_sent_finished_emails == False:

        debate.has_sent_finished_emails = True
        db.session.commit()

        if debate.pro_votes > debate.con_votes:
            try:
                votes = {
                    "opponent": debate.con_votes,
                    "recipient": debate.pro_votes
                }

                if user_pro.send_debate_finished_emails == True:
                    send_email(
                        generate_debate_complete_email(True, debate, user_pro.name,
                                                       user_con.name, votes),
                    user_pro.email)

                votes = {
                    "opponent": debate.pro_votes,
                    "recipient": debate.con_votes
                }

                if user_con.send_debate_finished_emails == True:
                    send_email(
                        generate_debate_complete_email(False, debate, user_con.name,
                                                       user_pro.name, votes),
                    user_con.email)
            except:
                pass

        elif debate.con_votes > debate.pro_votes:
            try:
                votes = {
                    "opponent": debate.con_votes,
                    "recipient": debate.pro_votes
                }

                if user_pro.send_debate_finished_emails == True:
                    send_email(
                        generate_debate_complete_email(False, debate, user_pro.name,
                                                       user_con.name, votes),
                    user_pro.email)

                votes = {
                    "opponent": debate.pro_votes,
                    "recipient": debate.con_votes
                }

                if user_con.send_debate_finished_emails == True:
                        send_email(
                            generate_debate_complete_email(True, debate, user_con.name,
                                                           user_pro.name, votes),
                        user_con.email)
            except:
                pass

        else:
            try:
                if user_pro.send_debate_finished_emails == True:
                    send_email(
                        generate_debate_complete_tied_email(debate, user_pro.name, user_con.name),
                    user_pro.email)

                if user_con.send_debate_finished_emails == True:
                    send_email(
                        generate_debate_complete_tied_email(debate, user_con.name, user_pro.name),
                    user_con.email)
            except:
                pass


def manage_email_transitions(debate, user_pro, user_con):
    if debate.stage == "voting":
        if (user_pro is not None) and (user_pro.send_voting_notification_emails == True):
            send_email(
                generate_voting_session_email(debate, user_pro.name, user_con.name),
                user_pro.email)
        if (user_con is not None) and (user_con.send_voting_notification_emails == True):
            send_email(
                generate_voting_session_email(debate, user_con.name, user_pro.name),
                user_con.email)
    elif debate.stage == "con":
        if (user_con is not None) and (user_con.send_round_continue_emails == True):
            send_email(
                generate_round_continue_email(debate, user_con.name, user_pro.name),
                user_con.email)
    elif debate.stage == "pro":
        if (user_pro is not None) and (user_pro.send_round_continue_emails == True):
            send_email(
                generate_round_continue_email(debate, user_pro.name, user_con.name),
                user_pro.email)


def move_to_voting_mode_if_finished(debate):
    if debate.current_round_number > debate.max_round_number:
        debate.stage = "voting"
        debate.pro_votes = 0
        debate.con_votes = 0
        if (debate.isTimed == None) or (debate.isTimed == "timed"):
            debate.time_for_next_phase = datetime.datetime.utcnow() + \
                                         datetime.timedelta(minutes=(main.config["TIME_DELTA"] * 2))
        elif debate.isTimed == "untimed":
            debate.time_for_next_phase = datetime.datetime.utcnow() + \
                                         datetime.timedelta(days=3)


def switch_from_pro_to_con(debate):
    if debate.stage == "pro":
        debate.stage = "con"

    elif debate.stage == "con":
        debate.stage = "pro"
        debate.current_round_number += 1

    if (len(debate.users) == 2) and ((debate.isTimed == None) or (debate.isTimed == "timed")):
        debate.time_for_next_phase = datetime.datetime.utcnow() + \
                                     datetime.timedelta(minutes=main.config["TIME_DELTA"])


def append_all_claims(debate, claim_support_form):
    claim = Claim()
    claim.enthymeme_claim = claim_support_form.claim_1.data
    claim.enthymeme_justification = claim_support_form.support_1.data
    claim.round_number = debate.current_round_number
    claim.user_type = debate.stage
    debate.claims.append(claim)


@main.route("/debates/debate_synopsis/<debate_id>", methods=["GET", "POST"])
def debate_synopsis(debate_id):
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

    debate = Debate.query.filter_by(id=debate_id).first()

    debate_key = "has_viewed" + str(debate.id)
    if debate_key in session:
        pass
    else:
        session[debate_key] = False

    if session[debate_key] == False:
        debate.views += 1
        db.session.commit()
        session[debate_key] = True

    mrn = debate.max_round_number

    rounds = return_rounds_of_debate(debate)

    user_pro, user_con = find_user_debate_stance(debate)

    if current_user.is_authenticated and current_user is not None:

        template_payload["is_vip"] = current_user.isVIP

        challenger = User.query.filter_by(id=current_user.id).first()

        template_payload["user"] = g.user

        # if debate is joinable and the current_user isn't in it, render the
        # join form and add the current_user upon validation
        if len(debate.users) < 2 and debate.users[0].user is not challenger:
            join_debate_form = JoinDebate()

            template_payload["join_debate_form"] = join_debate_form

            if join_debate_form.validate_on_submit():

                # check again in case of someone else joining in the meantime
                if len(debate.users) < 2 and debate.users[0].user is not challenger:
                    incumbent_user_type = debate.users[0].user_type

                    if incumbent_user_type == "pro":
                        add_user_to_debate(debate, challenger, user_type="con")
                    elif incumbent_user_type == "con":
                        add_user_to_debate(debate, challenger, user_type="pro")

                    if (debate.isTimed == "timed") or (debate.isTimed == None):
                        debate.time_for_next_phase = datetime.datetime.utcnow() + \
                                                     datetime.timedelta(minutes=main.config["TIME_DELTA"])

                    db.session.commit()

                    if debate.users[0].user.send_user_joined_emails == True:
                        send_email(
                            generate_user_joined_debate_email(debate, challenger.name,
                                                              challenger.avatar),
                            debate.users[0].user.email
                        )

                    return redirect(url_for("debate_synopsis",
                                            debate_id=debate_id))

            else:
                template_payload["rounds"] = rounds
                template_payload["max_round_number"] = mrn
                template_payload["debate_topic"] = debate.topic
                template_payload["user_pro"] = user_pro
                template_payload["user_con"] = user_con
                template_payload["round_num"] = debate.current_round_number
                template_payload["debate_id"] = debate_id
                template_payload["debate_stage"] = debate.stage

                # this, unfortunately, has to stay here because it stops execution from going to
                # the below claim_support_form stuff. It's ugly, but, hey. This file used to have
                # 4 render_templates!
                return render_template("debate_synopsis.html", server_data=template_payload)

        for u in debate.users:
            if current_user.id == u.user_id:
                if debate.stage == u.user_type:
                    claim_support_form = ClaimSupport()

                    template_payload["claim_support_form"] = claim_support_form

                    if claim_support_form.validate_on_submit():

                        if debate.stage != u.user_type:
                            return redirect(url_for("debate_synopsis",
                                                    debate_id=debate_id))

                        append_all_claims(debate, claim_support_form)
                        switch_from_pro_to_con(debate)
                        move_to_voting_mode_if_finished(debate)
                        db.session.commit()

                        if debate.isTimed == "untimed":
                            manage_email_transitions(debate, user_pro, user_con)

                        return redirect(url_for("debate_synopsis",
                                                debate_id=debate_id))

        canVote = False

        if (debate.stage == "voting") and (current_user not in debate.users_voted):
                canVote = True
                session["voting_status"] = {
                    "canVote": canVote,
                    "debate_id": debate_id
                }

    else:
        canVote = False
        template_payload["auth_url"] = g.auth_url

    try:
        if (debate.time_for_next_phase < datetime.datetime.utcnow()):
            if (debate.stage == "voting"):
                debate.stage = "finished"

                debate.current_round_number += 1

                if debate.pro_votes > debate.con_votes:
                    user_pro.wins += 1
                    user_con.losses += 1

                elif debate.con_votes > debate.pro_votes:
                    user_con.wins += 1
                    user_pro.losses += 1

            elif (user_pro is not None) and (user_con is not None):
                if (debate.stage == "pro") or (debate.stage == "con"):

                    switch_from_pro_to_con(debate)

                    claim = Claim()
                    claim.enthymeme_claim = " "
                    claim.enthymeme_justification = " "
                    claim.round_number = debate.current_round_number
                    claim.user_type = debate.stage
                    debate.claims.append(claim)

            db.session.commit()
            manage_debate_end_emails(debate, user_pro, user_con)
    except:
        print("ERROR")


    if (debate.stage == "voting" or debate.stage == "finished"):
        template_payload["pro_votes"] = debate.pro_votes
        template_payload["canVote"] = canVote
        template_payload["con_votes"] = debate.con_votes

        try:
            template_payload["user"] = challenger
        except:
            template_payload["user"] = None

    template_payload["rounds"] = rounds
    template_payload["max_round_number"] = mrn
    template_payload["round_num"] = debate.current_round_number
    template_payload["debate_topic"] = debate.topic
    template_payload["user_pro"] = user_pro
    template_payload["user_con"] = user_con
    template_payload["debate_id"] = debate_id
    template_payload["debate_stage"] = debate.stage
    template_payload["is_timed"] = debate.isTimed

    template_payload["debate_time"] = debate.time_for_next_phase

    return render_template("debate_synopsis.html", server_data=template_payload)
