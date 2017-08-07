from flask import render_template

def generate_user_joined_debate_email(debate, opponent_name, opponent_pic):
    return [
        "An opponent joined your debate!",
        render_template("emails/user_join_debate.html", debate=debate, opponent_name=opponent_name,
                        opponent_pic=opponent_pic),
        render_template("emails/user_join_debate.txt", debate=debate, opponent_name=opponent_name,
                        opponent_pic=opponent_pic)
    ]


def generate_round_continue_email(debate, recipient_name, opponent_name):
    return [
        "Your opponent has submitted their argument for this round!",
        render_template("emails/round_continue.html", debate=debate, recipient_name=recipient_name,
                        opponent_name=opponent_name),
        render_template("emails/round_continue.txt", debate=debate, recipient_name=recipient_name,
                        opponent_name=opponent_name)
    ]

def generate_voting_session_email(debate, recipient_name, opponent_name):
    return [
        "Your debate has moved into voting mode!",
        render_template("emails/voting_begun.html", debate=debate, recipient_name=recipient_name,
                        opponent_name=opponent_name),
        render_template("emails/voting_begun.txt", debate=debate, recipient_name=recipient_name,
                        opponent_name=opponent_name)
    ]

def generate_debate_complete_email(win_or_loss, debate, recipient_name, opponent_name, votes):
    return [
        "Voting has concluded on your debate!",
        render_template("emails/debate_complete.html", win=win_or_loss, debate=debate,
                        recipient_name=recipient_name, opponent_name=opponent_name, votes=votes),
        render_template("emails/debate_complete.txt", win=win_or_loss, debate=debate,
                        recipient_name=recipient_name, opponent_name=opponent_name, votes=votes)
    ]

def generate_debate_complete_tied_email(debate, recipient_name, opponent_name):
    return [
        "Voting has concluded on your debate!",
        render_template("emails/debate_complete_tied.html", debate=debate,
                        recipient_name=recipient_name, opponent_name=opponent_name),
        render_template("emails/debate_complete_tied.txt", debate=debate,
                        recipient_name=recipient_name, opponent_name=opponent_name)
    ]

def generate_greetings_email():
    return [
        "A thank you from the debateGate community",
        render_template("emails/greeting.html"),
        render_template("emails/greeting.txt")
    ]
