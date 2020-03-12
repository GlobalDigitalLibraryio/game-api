from flask_restplus import Resource, Namespace, fields
from language_tags import tags
from gdl_config import GDLConfig

API = GDLConfig.LANGUAGE_API

language = API.model('Language', {
    'code': fields.String(required=True, description='The BCP47 code used to represent the language'),
    'description': fields.String(required=False, description='Information about the language')
})


@API.route('/', strict_slashes=False)
class LanguageController(Resource):

    @API.doc('List of available languages')
    @API.marshal_with(language, True)
    def get(self):
        languages = [item['language'] for item in GDLConfig.GAMES_TABLE.scan()['Items']]
        unique = list(dict.fromkeys(languages))
        return [{'code': x, 'description': ', '.join(tags.description(x))} for x in unique]
