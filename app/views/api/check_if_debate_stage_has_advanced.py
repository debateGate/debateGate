from flask import jsonify

from app.models import Debate
from app.main import main

# ex:
#    https://www.debategate.net/api/has-debate-moved-on-boolean/1/2/pro;
#    json response: {"moved_on": true}
@main.route("/api/has-debate-moved-on-boolean/<int:debate_id>/<int:round_num>/<stage>")
def had_debate_moved_on_boolean(debate_id, round_num, stage):

    debate = Debate.query.filter_by(id=debate_id).first()

    if (debate.current_round_number == round_num) and (debate.stage == stage):
        return jsonify({"moved_on": False})
    return jsonify({"moved_on": True})
