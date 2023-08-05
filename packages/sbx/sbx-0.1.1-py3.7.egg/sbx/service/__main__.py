import os
import sys
from flask import Flask, jsonify, request, render_template
from werkzeug.security import safe_join

from ..core.card import Card
from ..core.study import CardStack
from ..core.utility import unix_str

api = Flask(__name__)
PATH = os.path.abspath(os.path.curdir)


def pack_card(card):
    path = os.path.relpath(card.path, PATH)
    meta_data = card.meta.to_dict()
    card_data = {}
    card_data["name"] = path
    card_data["reps"] = meta_data["reps"]
    card_data["last_studied_datetime"] = unix_str(meta_data["last"])
    card_data["scheduled_datetime"] = unix_str(meta_data["next"])
    card_data["is_leech"] = card.leech
    card_data["past_marks"] = meta_data["pastq"]
    card_data["is_last_mark_zero"] = card.zero
    card_data["scheduled_for_today"] = card.today
    return card_data


def get_card():
    name = request.args.get('name')
    if not name:
        return jsonify({}), 404
    card = Card(safe_join(PATH, name))
    card_data = pack_card(card)
    card_data["front"] = card.front
    card_data["back"] = card.back
    return jsonify(card_data), 200


def create_card():
    pass


def mark_card():
    pass


CARD_ROUTE = {"GET": get_card, "POST": create_card, "PUT": mark_card}


@api.route("/card", methods=("GET", "POST", "PUT"))
def card():
    return CARD_ROUTE[request.method]()


def list_cards():
    cstack = CardStack(PATH, recursive=True, include_unscheduled=True)
    return list(cstack.iter())


@api.route("/cards", methods=("GET", ))
def get_cards():
    return jsonify({"cards": [pack_card(x) for x in list_cards()]}), 200


@api.route("/")
def web_ui():
    return render_template('index.html', cards=list_cards())


@api.context_processor
def processors():
    def fix_path(path):
        return os.path.relpath(path, PATH)
    return dict(fix_path=fix_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a path as argument. python -m sbx.service PATH")
        sys.exit(-1)
    PATH = os.path.abspath(sys.argv[1])
    api.run(
        debug=False,
        use_debugger=False,
        use_reloader=False,
        host="0.0.0.0",
        port=53124,
    )
