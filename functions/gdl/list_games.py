from boto3.dynamodb.conditions import Attr
from flask import jsonify
from language_tags import tags

from .game import Game


class ListGames:
    def __init__(self, games_table, image_api_client):
        self.games_table = games_table
        self.image_api_client = image_api_client

    def main(self, request):
        tag = tags.tag(request.args.get('language'))
        items = self.games_table.scan(
            FilterExpression=Attr('language').eq(str(tag))) if tag.valid else self.games_table.scan()
        games = [Game.apply_defaults(x).api_response(self.image_api_client) for x in items['Items']]
        return jsonify(games)
