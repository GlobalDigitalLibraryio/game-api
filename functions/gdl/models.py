import uuid
from flask_restplus import fields
from language_tags import tags
from model.License import License
from licenses import license_dict
from gdl_config import GDLConfig


class ValidationError(ValueError):
    field_doc = {
        'message': fields.String(required=False, description='Description of the error'),
        'errors': fields.Raw(description='Detailed information about fields that did not pass validation')
    }

    model = GDLConfig.GAMES_API_V2.model('ValidationError', field_doc)

    def __init__(self, message, errors=None):
        self.errors = {} if errors is None else errors
        self.message = message

    def json(self):
        error_dict = {
            'message': self.message
        }

        if self.errors:
            error_dict['errors'] = self.errors

        return error_dict


class Game:
    @staticmethod
    def validate(api_input):
        errors = {}
        language_tag = tags.tag(api_input['language'])
        if not language_tag.valid:
            errors['language'] = '{} is not a supported language.'.format(api_input['language'])

        license = api_input['license']
        if license.lower() not in license_dict:
            errors['license'] = '{} is not a valid license.'.format(license)

        if len(errors) > 0:
            raise ValidationError('Input payload validation failed', errors=errors)

    @staticmethod
    def to_db_structure(api_input):
        Game.validate(api_input)

        return {
            'game_uuid': api_input.get('game_uuid', str(uuid.uuid4())),
            'external_id': api_input['external_id'],
            'title': api_input['title'],
            'description': api_input['description'],
            'language': tags.tag(api_input['language']).format,
            'url': api_input['url'],
            'license': api_input['license'],
            'source': api_input['source'],
            'publisher': api_input['publisher'],
            'coverimage': api_input['coverimage']['imageId']
        }

    @staticmethod
    def to_api_structure(db_output):
        api_response = {
            'game_uuid': db_output['game_uuid'],
            'external_id': db_output['external_id'],
            'title': db_output['title'],
            'description': db_output['description'],
            'language': tags.tag(db_output['language']).format,
            'url': db_output['url'],
            'source': db_output['source'],
            'publisher': db_output['publisher']
        }
        cover_image_details = GDLConfig.IMAGE_API_CLIENT.metadata_for(db_output['coverimage'])
        if cover_image_details:
            api_response['coverimage'] = cover_image_details.as_dict()

        license_details = License.medadata_for(db_output['license'])
        if license_details:
            api_response['license'] = license_details

        return api_response
