from flask import jsonify

from .game import Game


class AddGame:
    def __init__(self, games_table):
        self.games_table = games_table

    def main(self, game_dict):
        to_add = Game.apply_defaults(game_dict).to_dict()
        self.games_table.put_item(Item=to_add)
        return jsonify(to_add)
