import flask
from flask_restplus import Resource, Namespace, fields
from language_tags import tags

from game_repository import GameRepository
from gdl_config import GDLConfig

API = Namespace('games', description='Game related operations')

cover_image = API.model('CoverImage', {
    'imageId': fields.Integer(required=True, description='Unique identifier of the image'),
    'url': fields.String(required=False, description='The url for where the image can be downloaded'),
    'alttext': fields.String(required=False, description='An alternative text for the image')
})

game = API.model('Game', {
    'game_uuid': fields.String(required=False, description='The unique identifier for this Game'),
    'external_id': fields.String(required=True, description='Vendor ID for the game'),
    'title': fields.String(required=True, description='The title of the game'),
    'description': fields.String(required=True, description='A description of the game'),
    'language': fields.String(required=True, description='In which language the game is. Represented as a BCP47 tag'),
    'url': fields.String(required=True, description='The url for where the game is found'),
    'license': fields.String(required=True, description='Licensing information about the game'),
    'source': fields.String(required=True, description='From whom GDL has aquired the game'),
    'publisher': fields.String(required=True, description='The publisher of the game'),
    'coverimage': fields.Nested(cover_image, required=True, skip_none=True,
                                description='Information about the cover image of the game')
})

validation_error = API.model('ValidationError', {
    'message': fields.String(required=False, description='Description of the error'),
    'errors': fields.Raw(description='Detailed information about fields that did not pass validation')
})

game_repository = GameRepository(GDLConfig.GAMES_TABLE)


@API.route('/', strict_slashes=False)
class Games(Resource):

    @API.doc('List of available games', params={'language': 'Optional BCP47 language code to filter results'})
    @API.marshal_list_with(game, skip_none=True)
    def get(self):
        lang = flask.request.args.get('language')
        return game_repository.all_with_language(lang) if lang else game_repository.all()

    @API.doc('Add a game', security='oauth2')
    @API.marshal_with(game)
    @API.expect(game, validate=True)
    @API.response(code=400, description='When a validation error occurs', model=validation_error)
    @API.response(code=403, description='Not authorized')
    def post(self):
        GDLConfig.JWT_VALIDATOR.verify_role(flask.request, 'games:write', API)
        return game_repository.add(API.payload)


@API.route("/<string:game_uuid>", strict_slashes=False)
class Gamer(Resource):

    @API.doc('Get information about a single game')
    @API.marshal_with(game)
    @API.response(code=404, description='Not Found')
    def get(self, game_uuid):
        response = game_repository.with_uuid(game_uuid)
        return response if response else \
            API.abort(404, "Game with id {} was not found.".format(game_uuid))

    @API.doc('Update information about a game', security='oauth2')
    @API.expect(game, validate=True)
    @API.marshal_with(game)
    @API.response(code=400, description='When a validation error occurs', model=validation_error)
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

