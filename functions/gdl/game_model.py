from flask_restplus import Namespace, fields

API = Namespace('games', description='Game related operations')

class CoverImage:
    field_doc = {
        'imageId': fields.Integer(required=True, description='Unique identifier of the image'),
        'url': fields.String(required=False, description='The url for where the image can be downloaded'),
        'alttext': fields.String(required=False, description='An alternative text for the image')
    }

    model = API.model('CoverImage', field_doc)

    def __init__(self, imageId, url, alttext):
        self.__imageId = imageId
        self.__url = url
        self.__alttext = alttext

    @property
    def imageId(self):
        return self.__imageId

    @property
    def url(self):
        return self.__url

    @property
    def alttext(self):
        return self.__alttext


class Language:
    field_doc = {
        'code': fields.String(required=True, description="BCP47 language code"),
        'name': fields.String(required=True, description="Language description of language code")
    }

    model = API.model('Language', field_doc)

    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name


class Game:
    field_doc = {
        'game_uuid': fields.String(required=False, description='The unique identifier for this Game'),
        'external_id': fields.String(required=True, description='Vendor ID for the game'),
        'title': fields.String(required=True, description='The title of the game'),
        'description': fields.String(required=True, description='A description of the game'),
        'language': fields.String(required=True, description='In which language the game is. Represented as a BCP47 tag'),
        'url': fields.String(required=True, description='The url for where the game is found'),
        'license': fields.String(required=True, description='Licensing information about the game'),
        'source': fields.String(required=True, description='From whom GDL has aquired the game'),
        'publisher': fields.String(required=True, description='The publisher of the game'),
        'coverimage': fields.Nested(CoverImage.model, required=True, skip_none=True, description='Information about the cover image of the game')
    }

    model = API.model('Game', field_doc)

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

    model = API.model('GameResponse', field_doc)

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



