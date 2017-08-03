"""
Contains all queries, as opposed to db_exec.py, which contains critical database
write operations.
"""

import string

from sqlalchemy import desc

from app.lib.utilities import paginate_list

from app.models import Debate, UserDebate, Claim
from app.lib.constants import SEARCH_TYPES, COMMON_WORDS

from app.main import main


def find_user_debate_stance(debate):
    """Given a debate, get both the pro and con user"""
    user_pro = None
    user_con = None

    try:
        user_pro = UserDebate.query.filter(
                                           (UserDebate.debate_id == debate.id),
                                           (UserDebate.user_type == "pro")
                                          ).first().user
    except AttributeError:
        pass

    try:
        user_con = UserDebate.query.filter(
                                           (UserDebate.debate_id == debate.id),
                                           (UserDebate.user_type == "con")
                                          ).first().user
    except AttributeError:
                pass

    return user_pro, user_con


def search_debates(searchtype="in-progress", terms="", page=1, isGlobalSearch=False):
    """Debate search algorithm."""

    translator = str.maketrans('', '', string.punctuation)

    if terms == "___blank___":
        terms = ""

    debates = []
    terms = terms.translate(translator)
    term_list = terms.split()

    for term in term_list:
        if term.lower() in COMMON_WORDS:
            term_list.remove(term.lower())

    for debate in Debate.query.all():

        topic = debate.topic
        topic = topic.lower()
        topic = topic.translate(translator)

        if len(term_list) == 0:
            weight = 999999
        else:
            weight = 0

        #if (len(debate.users) == SEARCH_TYPES[searchtype]) or (debate.stage == "archived"):
        if len(debate.users) == 1:
            debate_stage = "joinable"
        elif debate.stage == "finished" or debate.stage == "pro" or debate.stage == "con" or debate.stage == "voting":
            debate_stage = "in-progress"
        else:
            debate_stage = "archived"

        if debate_stage == searchtype:
            for term in term_list:
                if term.lower() in topic.split():
                    weight += 1

            if weight > 0:
                user_pro, user_con = find_user_debate_stance(debate)
                i = {
                    "id": debate.id,
                    "user_pro": user_pro,
                    "topic": debate.topic,
                    "current_round_number": debate.current_round_number,
                    "max_round_number": debate.max_round_number,
                    "user_con": user_con,
                    "is_timed": debate.isTimed,
                    "views": debate.views,
                    "stage": debate.stage,
                    "weight": weight
                }
                debates.append(i)

    if (searchtype == "in-progress") and (isGlobalSearch == False):
        debates = sorted(debates, key=lambda d: d["views"], reverse=True)

    elif (terms == ""):
        debates = sorted(debates, key=lambda d: d["views"], reverse=True)

    else:
        debates = sorted(debates, key=lambda d: d["weight"], reverse=True)

    debates = list(paginate_list(debates, main.config["POSTS_PER_PAGE"]))
    len_of_page_list = len(debates)

    try:
        debates = debates[page - 1]
    except(IndexError):
        debates = []

    return (debates, len_of_page_list)


def return_rounds_of_debate(debate):
    """
    This loop block gets all the claims in order; it assumes the list is
    already sorted by round number, and then again by pro/con, (descending,
    so pro comes first) so the list should look like this:

    round 1 pro
    round 1 pro
    round 1 pro
    round 1 con
    round 1 con
    round 2 pro
    round 2 pro
    round 2 con
    ... etc. etc.

    It packages all this into a data structure that the template assumes
    looks like:

    [ <-- the whole array
     [ <-- each one of these is a round
        [ <-- pro
            { <-- individual claim
                claim: x,
                support: y
            },
            {
                claim: z,
                support: w
            }
        ],

        [ <-- con
            { <--individual claim
                claim: j,
                support: a
            },
            {
                claim: k,
                support: p
            }
        ]
     ],
    ]
    """

    rounds = []
    current_round_number = -1

    # for every claim in the debate, ordered by the scheme outlined above
    for c in Claim.query.filter_by(debate_id=debate.id).order_by(
                                          Claim.round_number,
                                          desc(Claim.user_type)
                                         ):
        if not (current_round_number == c.round_number):
            current_round_number = c.round_number
            rounds.append([[], []])

        i = c.round_number - 1

        if c.user_type == "pro":
            rounds[i][0].append(
                {
                    "claim": c.enthymeme_claim,
                    "support": c.enthymeme_justification
                }
            )
        elif c.user_type == "con":
            rounds[i][1].append(
                {
                    "claim": c.enthymeme_claim,
                    "support": c.enthymeme_justification
                }
            )

    return rounds
