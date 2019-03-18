import uuid
from jsonschema import FormatChecker
from language_tags import tags

class Game:
    schema = {
        'type': 'object',
        'properties': {
            'game_uuid': {'type': 'string'},
            'external_id': {'type': 'string'},
            'title': {'type': 'string'},
            'description': {'type': 'string'},
            'language': {'type': 'string', 'format': 'bcp47'},
            'url': {'type': 'string'},
            'license': {'type': 'string'},
            'source': {'type': 'string'},
            'publisher': {'type': 'string'},
            'coverphoto': {'type': 'string'},
        },
        'required': ['external_id', 'title', 'description', 'language', 'url', 'license', 'source', 'publisher',
                     'coverphoto']
    }

    format_checker = FormatChecker()

    @staticmethod
    @format_checker.checks('bcp47')
    def is_bcp_47(value):
        return tags.tag(value).valid


    def __init__(self, external_id, title, description, language, url, license, source, publisher, coverphoto,
                 game_uuid=str(uuid.uuid4())):
        self.game_uuid = game_uuid
        self.external_id = external_id
        self.title = title
        self.description = description
        self.language = language
        self.url = url
        self.license = license
        self.source = source
        self.publisher = publisher
        self.coverphoto = coverphoto

    @staticmethod
    def apply_defaults(game_dict):
        return Game(external_id=game_dict['external_id'],
                    title=game_dict['title'],
                    description=game_dict['description'],
                    language=tags.tag(game_dict['language']).format,
                    url=game_dict['url'],
                    license=game_dict['license'],
                    source=game_dict['source'],
                    publisher=game_dict['publisher'],
                    coverphoto=game_dict['coverphoto'],
                    game_uuid=game_dict.get('game_uuid', str(uuid.uuid4())))

    def to_dict(self):
        return {
            'game_uuid': self.game_uuid,
            'external_id': self.external_id,
            'title': self.title,
            'description': self.description,
            'language': self.language,
            'url': self.url,
            'license': self.license,
            'source': self.source,
            'publisher': self.publisher,
            'coverphoto': self.coverphoto
        }