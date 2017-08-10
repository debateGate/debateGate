""" Contains all database models. """

from flask_login import UserMixin

from app.main import db


class UserDebate(db.Model):
    """Associates users with the debates they're in."""

    __tablename__ = "user_debate"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),
                        primary_key=True)
    debate_id = db.Column(db.Integer, db.ForeignKey("debates.id"),
                          primary_key=True)
    user_type = db.Column(db.String(10))
    debate = db.relationship("Debate", back_populates="users")
    user = db.relationship("User", back_populates="debates")


# Direct table (as opposed to a model object class) to link the users with their votes
user_vote_tally = db.Table("user_vote_tally", db.metadata,
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('debate_id', db.Integer, db.ForeignKey('debates.id')))


class User(db.Model, UserMixin):
    """Table for all user data, because I'm lazy and scared of making new tables
    and also of refactoring but we can ignore that part"""

    __tablename__ = "users"

    # OAuth columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.Text)
    isVIP = db.Column(db.Boolean, default=False)

    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)

    debates = db.relationship("UserDebate", back_populates="user")
    debates_voted = db.relationship("Debate", secondary=user_vote_tally, back_populates="users_voted")
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    #email settings
    send_user_joined_emails = db.Column(db.Boolean, default=True)
    send_round_continue_emails = db.Column(db.Boolean, default=True)
    send_voting_notification_emails = db.Column(db.Boolean, default=True)
    send_debate_finished_emails = db.Column(db.Boolean, default=True)

    #sync with google
    sync_with_google = db.Column(db.Boolean, default=True)


class Debate(db.Model):
    """Pretty much a catch-all table for anything related to a debate at this point."""

    __tablename__ = "debates"

    id = db.Column(db.Integer, primary_key=True)

    views = db.Column(db.Integer)

    dtype = db.Column(db.String(40))
    topic = db.Column(db.String(100))

    current_round_number = db.Column(db.Integer)
    stage = db.Column(db.String(10))
    max_round_number = db.Column(db.Integer)
    max_claim_number = db.Column(db.Integer)

    isTimed = db.Column(db.String(10))
    time_for_next_phase = db.Column(db.DateTime)

    pro_votes = db.Column(db.Integer)
    con_votes = db.Column(db.Integer)

    definitions = db.relationship("Definition", backref="Debate")
    claims = db.relationship("Claim", backref="Debate")
    users = db.relationship("UserDebate", back_populates="debate", cascade="all, delete-orphan")
    users_voted = db.relationship("User", secondary=user_vote_tally, back_populates="debates_voted")
    has_sent_finished_emails = db.Column(db.Boolean, default=False)

class Definition(db.Model):
    """Table for the implementation of definitions."""

    __tablename__ = "definitions"

    id = db.Column(db.Integer, primary_key=True)
    debate_id = db.Column(db.Integer, db.ForeignKey("debates.id"))

    term = db.Column(db.String(25))
    body = db.Column(db.String(500))


class Claim(db.Model):
    """Table for the storage of claims."""

    __tablename__ = "claims"

    id = db.Column(db.Integer, primary_key=True)
    debate_id = db.Column(db.Integer, db.ForeignKey("debates.id"))
    opposing_claim_id = db.Column(db.Integer, db.ForeignKey("claims.id"))

    enthymeme_claim = db.Column(db.String(1500))
    enthymeme_justification = db.Column(db.String(1500))
    round_number = db.Column(db.Integer)
    user_type = db.Column(db.String(10))
