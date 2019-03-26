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
from gdl.jwt_validate import JWTValidator, MissingRoleError
from gdl.integration.image_api_client import ImageApiClient


def get_dynamodb(is_offline):
    if is_offline:
        return boto3.resource('dynamodb', region_name='localhost', endpoint_url=os.environ['LOCAL_DYNAMODB'])

    return boto3.resource('dynamodb')


is_offline = os.getenv('IS_OFFLINE', False)
dynamodb = get_dynamodb(is_offline)
games_table = dynamodb.Table(os.environ['GAMES_TABLE'])
gdl_environment = os.getenv('GDL_ENVIRONMENT', 'prod')
image_api_address = os.environ['IMAGE_API_OFFLINE_ADDRESS'] if is_offline else 'http://image-api.gdl-local'

app = Flask(__name__)
app.config['JSON_SCHEMA_FORMAT_CHECKER'] = Game.format_checker
schema = JsonSchema(app)
jwt = JWTValidator(gdl_environment)

image_api_client = ImageApiClient(image_api_address)


@app.route("/game-service/v1/languages")
def languages():
    return ListLanguages(games_table).main()


@app.route("/game-service/v1/games")
def games():
    return ListGames(games_table, image_api_client).main(request)


@app.route("/game-service/v1/games", methods=["POST"])
@schema.validate(Game.schema)
@jwt.require_role(request, role="games:write")
def create():
    return AddGame(games_table).main(request.get_json())


@app.route("/game-service/v1/games/<string:game_uuid>")
def read(game_uuid):
    return GetGame(games_table, image_api_client).main(game_uuid)


@app.route("/game-service/v1/games/<string:game_uuid>", methods=["PUT"])
@schema.validate(Game.schema)
@jwt.require_role(request, role="games:write")
def update(game_uuid):
    return UpdateGame(games_table).main(game_uuid, request.get_json())


@app.route("/game-service/v1/games/<string:game_uuid>", methods=["DELETE"])
@jwt.require_role(request, role="games:write")
def delete(game_uuid):
    return DeleteGame(games_table).main(game_uuid)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    return make_response(
        jsonify({'error': e.message, 'errors': [validation_error.message for validation_error in e.errors]}), 400)


@app.errorhandler(MissingRoleError)
def authorization_error(e):
    return make_response(jsonify({'error': e.message}), 403)


if __name__ == "__main__":
    app.run()
