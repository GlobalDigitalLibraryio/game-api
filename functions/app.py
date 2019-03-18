import os

import boto3
from flask import Flask, request, jsonify, make_response
from flask_json_schema import JsonSchema, JsonValidationError

from gdl.add_game import AddGame
from gdl.delete_game import DeleteGame
from gdl.game import Game
from gdl.get_game import GetGame
from gdl.list_games import ListGames
from gdl.list_languages import ListLanguages
from gdl.update_game import UpdateGame


def get_dynamodb(is_offline):
    if is_offline:
        return boto3.resource('dynamodb', region_name='localhost', endpoint_url=os.environ['LOCAL_DYNAMODB'])

    return boto3.resource('dynamodb')

dynamodb = get_dynamodb(os.getenv('IS_OFFLINE', False))
games_table = dynamodb.Table(os.environ['GAMES_TABLE'])

list_games = ListGames(games_table)
get_game = GetGame(games_table)
add_game = AddGame(games_table)
delete_game = DeleteGame(games_table)
list_languages = ListLanguages(games_table)
update_game = UpdateGame(games_table)

app = Flask(__name__)
app.config['JSON_SCHEMA_FORMAT_CHECKER'] = Game.format_checker
schema = JsonSchema(app)

@app.route("/v1/languages")
def languages():
    return list_languages.main()

@app.route("/v1/games")
def games():
    return list_games.main(request)

@app.route("/v1/games", methods=["POST"])
@schema.validate(Game.schema)
def create():
    return add_game.main(request.get_json())

@app.route("/v1/games/<string:game_uuid>")
def read(game_uuid):
    return get_game.main(game_uuid)

@app.route("/v1/games/<string:game_uuid>", methods=["PUT"])
@schema.validate(Game.schema)
def update(game_uuid):
    return update_game.main(game_uuid, request.get_json())

@app.route("/v1/games/<string:game_uuid>", methods=["DELETE"])
def delete(game_uuid):
    return delete_game.main(game_uuid)

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return make_response(jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]}), 400)

if __name__ == "__main__":
    app.run()
