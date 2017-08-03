"""
Contains all shared functions that modify the database; contrast this with
queries.py, which contains all shared functions that query the database only.
"""

from app.models import Debate, UserDebate
from app.main import db


def add_user_to_debate(debate, user, user_type):
    """ Adds a given user to a given debate with the given user_type"""

    association = UserDebate(user_type=user_type)
    association.user = user
    debate.users.append(association)

    if not Debate.query.filter_by(id=debate.id).first():
        db.session.add(debate)

    db.session.commit()


def add_user_to_votelist(debate, user):
    """ Adds a given user and debate to the vote table"""

    d = debate
    u = user

    d.users_voted.append(u)
    db.session.add(d)

    db.session.commit()
