import flask
from flask_restplus import Resource, Namespace, fields
from language_tags import tags
from game_model import Game, GameResponse

from game_repository import GameRepository
from gdl_config import GDLConfig

API = Namespace('games', description='Game related operations')


class ValidationError:
    field_doc = {
        'message': fields.String(required=False, description='Description of the error'),
        'errors': fields.Raw(description='Detailed information about fields that did not pass validation')
    }

    model = API.model('ValidationError', field_doc)

    def __init__(self, message, errors):
        self.__message = message
        self.__errors = errors

    @property
    def message(self):
        return self.__message

    @property
    def errors(self):
        return self.__errors
