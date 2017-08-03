""" Contains all forms and validations for those forms. """

from flask_wtf import Form
from wtforms import StringField, RadioField, SelectField, TextAreaField,\
        SubmitField
from wtforms.validators import DataRequired, Length, InputRequired


class DebateCreate(Form):
    debate_type = SelectField("debate_type", choices=[("1v1", "1 VS 1")],
                              validators=[DataRequired()])

    is_timed = SelectField("is_timed",
                           choices=[
                               ("untimed", "Untimed"),
                               ("timed", "Timed")
                           ], validators=[DataRequired()])

    topic = StringField("topic", validators=[DataRequired(),
                                             Length(min=8, max=100)])

    max_round_number = SelectField("max_round_number", choices=[
        (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)],
        coerce=int, validators=[DataRequired()])

    pro_or_con = RadioField("pro_or_con",
                            choices=[
                                ("pro", "Pro to the issue"),
                                ("con", "Con to the issue")
                            ], validators=[DataRequired()])


class EmailSettings(Form):
    send_user_joined_emails = RadioField("user_join",
                            choices=[
                                (1, "Yes"),
                                (0, "No")
                            ], coerce=int, validators=[InputRequired()])

    send_round_continue_emails = RadioField("round_continue",
                            choices=[
                                (1, "Yes"),
                                (0, "No")
                            ], coerce=int, validators=[InputRequired()])

    send_voting_notification_emails = RadioField("voting_notifs",
                            choices=[
                                (1, "Yes"),
                                (0, "No")
                            ], coerce=int, validators=[InputRequired()])

    send_debate_finished_emails = RadioField("debate_finished",
                            choices=[
                                (1, "Yes"),
                                (0, "No")
                            ], coerce=int, validators=[InputRequired()])


class DebateSearchBar(Form):
    search_bar = StringField("search_bar", validators=[
                                                      DataRequired(),
                                                      Length(max=150)
                                                      ])


class ClaimSupport(Form):
    claim_1 = TextAreaField("claim_1", validators=[
        Length(min=0, max=1500),
        DataRequired()
    ])
    support_1 = TextAreaField("support_1", validators=[
        Length(min=0, max=1500),
        DataRequired()
    ])


class JoinDebate(Form):
    button = SubmitField(label="Join Debate", validators=[DataRequired()])


class HomepageSearch(Form):
    search_bar = StringField("search_bar", render_kw={"placeholder": "Optional search"})
    debate_type = SelectField("debate_type", choices=[
        ("in-progress", "In Progress"),
        ("joinable", "Looking for Partner"),
        ("archived", "Finished")
    ],
    validators=[DataRequired()])

    button = SubmitField(label="Filter", validators=[DataRequired()])
