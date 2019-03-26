from flask import jsonify
from .game import Game
from . import not_found


class UpdateGame:

    def __init__(self, games_table):
        self.games_table = games_table

    def main(self, game_uuid, game_dict):
        result = self.games_table.get_item(Key={
            'game_uuid': game_uuid
        })

        item = result.get('Item')
        if item:
            to_update = Game.apply_defaults(game_dict).to_dict()
            to_update['game_uuid'] = game_uuid

            self.games_table.put_item(Item=to_update)
            return jsonify(to_update)
        else:
            return not_found("Game with id {} was not found".format(game_uuid))
