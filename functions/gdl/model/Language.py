from flask_restplus import fields
from gdl_config import GDLConfig

class Language:
    field_doc = {
        'code': fields.String(required=True, description="BCP47 language code"),
        'name': fields.String(required=False, description="Language description of language code if name exist")
    }

    model = GDLConfig.GAMES_API_V2.model('Language', field_doc)

    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name
