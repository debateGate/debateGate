#!flask/bin/python3
"""
This script is to be cronned every 30 minutes to cause continuations on in-progress
debates.

Copy to and run this from the main debateGate directory, not the script directory.
"""

import datetime

from app.main import db, main
from app.models import Debate
from app.lib.queries import find_user_debate_stance
from app.models import Claim

for debate in Debate.query.all():
    user_pro, user_con = find_user_debate_stance(debate)

    if (debate.time_for_next_phase is not None) and \
       (datetime.datetime.utcnow() > (debate.time_for_next_phase + datetime.timedelta(days=30))):
        db.session.delete(debate)
        continue


    if (debate.time_for_next_phase is not None) and (datetime.datetime.utcnow() > debate.time_for_next_phase):
        if debate.stage == "voting":
            debate.stage = "finished"
            debate.current_round_number += 1

            if debate.pro_votes > debate.con_votes:
                user_pro.wins += 1
                user_con.losses += 1
            elif debate.con_votes > debate.pro_votes:
                user_con.wins += 1
                user_pro.losses += 1


        if (debate.stage == "pro") or (debate.stage == "con"):
            claim = Claim()
            claim.enthymeme_claim = " "
            claim.enthymeme_justification = " "
            claim.round_number = debate.current_round_number
            claim.user_type = debate.stage
            debate.claims.append(claim)

            if debate.stage == "pro":
                debate.stage = "con"

            elif debate.stage == "con":
                debate.stage = "pro"
                debate.current_round_number += 1

            debate.time_for_next_phase = datetime.datetime.utcnow() + \
                                 datetime.timedelta(minutes=main.config["TIME_DELTA"])


        if (debate.current_round_number > debate.max_round_number) and (debate.stage != "finished"):
            debate.stage = "voting"
            debate.pro_votes = 0
            debate.con_votes = 0
            debate.time_for_next_phase = datetime.datetime.utcnow() + \
                                     datetime.timedelta(minutes=(main.config["TIME_DELTA"] * 2))


    if (debate.stage == "finished") and (datetime.datetime.utcnow() > debate.time_for_next_phase + datetime.timedelta(hours=3)):
        debate.stage = "archived"

db.session.commit()
