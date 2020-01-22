from flask_restplus import fields
from gdl_config import GDLConfig
from licenses import license_dict

class License:
    field_doc = {
        'name': fields.String(required=True, description='Unique identifier of the image'),
        'description': fields.String(required=False, description='The url for where the image can be downloaded'),
        'url': fields.String(required=False, description='An alternative text for the image')
    }

    model = GDLConfig.GAMES_API_V3.model('License', field_doc)

    def __init__(self, name, url, description):
        self.__name = name
        self.__url = url
        self.__description = description

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def description(self):
        return self.__description

    @staticmethod
    def medadata_for(license_name):
        license = license_dict[license_name.lower()]

        return {
            'name': license['name'],
            'description': license['description'],
            'url': license['url']
        }