from flask_restplus import fields
from gdl_config import GDLConfig

class CoverImage:
    field_doc = {
        'imageId': fields.Integer(required=True, description='Unique identifier of the image'),
        'url': fields.String(required=False, description='The url for where the image can be downloaded'),
        'alttext': fields.String(required=False, description='An alternative text for the image')
    }

    model = GDLConfig.GAMES_API_V2.model('CoverImage', field_doc)

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

