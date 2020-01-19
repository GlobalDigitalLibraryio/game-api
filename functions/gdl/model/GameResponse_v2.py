from flask_restplus import fields
from gdl_config import GDLConfig

from model.Language import Language
from model.Game import Game

class GameResponse:
    field_doc = {
        'totalCount': fields.Integer(required=True, description="Total amount of games."),
        'page': fields.Integer(required=True, description="The page number of the search hits to display."),
        'pageSize': fields.Integer(required=True, description="The number of search hits to display for each page."),
        'language': fields.Nested(Language.model, required=True, skip_none=True,
                                description='Language model'),
        'results': fields.List(
            fields.Nested(Game.model, required=True, description='Game data', skip_none=True), skip_none=True),
    }

    model = GDLConfig.GAMES_API_V2.model('GameResponse', field_doc)

    def __init__(self, totalCount, page, pageSize, language, results):
        self.__totalCount = totalCount
        self.__page = page
        self.__pageSize = pageSize
        self.__language = language
        self.__results = results

    @property
    def totalCount(self):
        return self.__totalCount

    @property
    def page(self):
        return self.__page

    @property
    def pageSize(self):
        return self.__pageSize

    @property
    def language(self):
        return self.__language

    @property
    def results(self):
        return self.__results



