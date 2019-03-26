from flask import jsonify

from . import not_found
from .game import Game


class GetGame:
    def __init__(self, games_table, image_api_client):
        self.games_table = games_table
        self.image_api_client = image_api_client

    def main(self, game_uuid):
        result = self.games_table.get_item(Key={
            'game_uuid': game_uuid
        })

        item = result.get('Item')
        if item:
            return jsonify(Game.apply_defaults(result['Item']).api_response(self.image_api_client))
        else:
            return not_found("Game with id {} was not found".format(game_uuid))
