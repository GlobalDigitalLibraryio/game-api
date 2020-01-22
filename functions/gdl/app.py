from flask import Flask, jsonify, Blueprint
from flask_restplus import Api, Resource, Namespace

import language_controller
import game_controller_v1
import game_controller_v2
import game_controller_v3
from gdl_config import GDLConfig

from models import ValidationError

blueprint = Blueprint('api', __name__)

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'implicit',
        'authorizationUrl': 'https://digitallibrary.eu.auth0.com/authorize',
        'scopes': {
            'games:all': 'Grant full access to games',
        }
    }
}

api = Api(blueprint, title="Game Service", description="Service for retrieving games from the GDL", authorizations=authorizations, version='1.0',
          terms_url='https://digitallibrary.io', contact='Christer Gundersen',
          contact_email='support@digitallibrary.io', contact_url='https://digitallibrary.io',
          license='Apache License 2.0', license_url='https://www.apache.org/licenses/LICENSE-2.0', doc=False)

api.add_namespace(language_controller.API, path='/v1/languages')
api.add_namespace(GDLConfig.GAMES_API_V1, path='/v1/games')
api.add_namespace(GDLConfig.GAMES_API_V2, path='/v2/games')
api.add_namespace(GDLConfig.GAMES_API_V3, path='/v3/games')

DOC_API = Namespace('api-docs', description="API Documentation for the API")


@DOC_API.route("/", strict_slashes=False)
@DOC_API.doc(False)
class ApiDocumentation(Resource):
    def get(self):
        swagger = api.__schema__
        swagger['basePath'] = '/game-service'
        return jsonify(api.__schema__)


docprint = Blueprint('doc', __name__)
docApi = Api(docprint, description="Documentation for APIs")
docApi.add_namespace(DOC_API, path='/')

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/'
app.register_blueprint(blueprint, url_prefix='/game-service', doc='/doc/')
app.register_blueprint(docprint, url_prefix='/game-service/api-docs')


@api.errorhandler(ValidationError)
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """When a validation error occurs"""
    return error.json(), 400


if __name__ == "__main__":
    app.run()
