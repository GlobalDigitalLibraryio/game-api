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
        return [{'code': x['language'], 'description': ', '.join(tags.description(x['language']))} for x in
                GDLConfig.GAMES_TABLE.scan()['Items']]
