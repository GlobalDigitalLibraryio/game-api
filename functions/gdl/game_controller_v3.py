"""
A version 3 of game_controller.py to allow backward compatibility for end users.
Changes in this file is an updated GAMES_API_V3 model that has a new License output.

TODO: delete deprecated version e.g game_controller.py and rename this file back to game_controller.py
"""
import flask
from flask_restplus import Resource, Namespace, fields
from language_tags import tags
from model.Game_v2 import Game
from model.GameResponse_v2 import GameResponse
from models_v2 import ValidationError

from game_repository_v2 import GameRepository
from gdl_config import GDLConfig

API = GDLConfig.GAMES_API_V3

game_repository = GameRepository(GDLConfig.GAMES_TABLE)


@API.route('/', strict_slashes=False)
class Games(Resource):

    @API.doc('List of available games', params={'language': 'Optional BCP47 language code to filter results', 'page': 'Return results for this page', 'page-size': 'Return this many results per page.' })
    @API.marshal_with(GameResponse.model, skip_none=True)
    def get(self):
        lang = flask.request.args.get('language', default='en')
        page = flask.request.args.get('page', default=1, type=int)
        page_size = flask.request.args.get('page-size', default=10, type=int)
        
        formatted_lang = tags.tag(lang).format
        lang_name = tags.description(lang)[0] if tags.check(lang) else None

        return game_repository.all_v2(formatted_lang, lang_name, page, page_size)

    @API.doc('Add a game', security='oauth2')
    @API.marshal_with(Game.model)
    @API.expect(Game.field_doc, validate=True)
    @API.response(code=400, description='When a validation error occurs', model=ValidationError.model)
    @API.response(code=403, description='Not authorized')
    def post(self):
        GDLConfig.JWT_VALIDATOR.verify_role(flask.request, 'games:write', API)
        return game_repository.add(API.payload)


@API.route("/<string:game_uuid>", strict_slashes=False)
class Gamer(Resource):

    @API.doc('Get information about a single game')
    @API.marshal_with(Game.model)
    @API.response(code=404, description='Not Found')
    def get(self, game_uuid):
        response = game_repository.with_uuid(game_uuid)
        return response if response else \
            API.abort(404, "Game with id {} was not found.".format(game_uuid))

    @API.doc('Update information about a game', security='oauth2')
    @API.expect(Game.field_doc, validate=True)
    @API.marshal_with(Game.model)
    @API.response(code=400, description='When a validation error occurs', model=ValidationError.model)
    @API.response(code=403, description='Not authorized')
    @API.response(code=404, description='Not Found')
    def put(self, game_uuid):
        GDLConfig.JWT_VALIDATOR.verify_role(flask.request, 'games:write', API)
        response = game_repository.update(game_uuid, API.payload)
        if not response:
            API.abort(404, "Game with id {} was not found".format(game_uuid))
        return response

    @API.doc('Delete a game', security='oauth2')
    def delete(self, game_uuid):
        GDLConfig.JWT_VALIDATOR.verify_role(flask.request, 'games:write', API)
        game_repository.delete(game_uuid)
        return '', 204


@API.route("/extern/<string:external_id>", strict_slashes=False)
@API.doc(False)
class InternGame(Resource):

    def get(self, external_id):
        response = game_repository.with_external_id(external_id)
        if not response:
            API.abort(404, "Game with external_id {} was not found.".format(external_id))
        return response

