from flask import jsonify, make_response
from .game import Game
from . import not_found

class GetGame:
    def __init__(self, games_table):
        self.games_table = games_table

    def main(self, game_uuid):
        result = self.games_table.get_item(Key={
            'game_uuid': game_uuid
        })

        item = result.get('Item')
        if item:
            return jsonify(Game.apply_defaults(result['Item']).to_dict())
        else:
            return not_found(message="Game with id {} was not found".format(game_uuid))
