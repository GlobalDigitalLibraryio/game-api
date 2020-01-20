"""
A version 2 of Game.py to allow backward compatibility for end users.
Changes in this file is an updated License model that has a new License output.

TODO: delete deprecated version e.g Game.py and rename this file back to Game.py
"""
from flask_restplus import fields
from gdl_config import GDLConfig
from model.License import License
from model.CoverImage import CoverImage

class Game:
    field_doc = {
        'game_uuid': fields.String(required=False, description='The unique identifier for this Game'),
        'external_id': fields.String(required=True, description='Vendor ID for the game'),
        'title': fields.String(required=True, description='The title of the game'),
        'description': fields.String(required=True, description='A description of the game'),
        'language': fields.String(required=True, description='In which language the game is. Represented as a BCP47 tag'),
        'url': fields.String(required=True, description='The url for where the game is found'),
        'license': fields.Nested(License.model, required=True, description='Licensing information about the game'),
        'source': fields.String(required=True, description='From whom GDL has aquired the game'),
        'publisher': fields.String(required=True, description='The publisher of the game'),
        'coverimage': fields.Nested(CoverImage.model, required=True, skip_none=True, description='Information about the cover image of the game')
    }

    model = GDLConfig.GAMES_API_V3.model('Game', field_doc)

    def __init__(self, game_uuid, external_id, title, description, language, url, license, source, publisher, coverimage):
        self.__game_uuid = game_uuid
        self.__external_id = external_id
        self.__title = title
        self.__description = description
        self.__language = language
        self.__url = url
        self.__license = license
        self.__source = source
        self.__publisher = publisher
        self.__coverimage = coverimage

    @property
    def game_uuid(self):
        return self.__game_uuid

    @property
    def external_id(self):
        return self.__external_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def language(self):
        return self.__language

    @property
    def url(self):
        return self.__url

    @property
    def license(self):
        return self.__license

    @property
    def source(self):
        return self.__source

    @property
    def publisher(self):
        return self.__publisher

    @property
    def coverimage(self):
        return self.__coverimage
