import requests
import logging
from . import ImageMetaData


class ImageApiClient:

    def __init__(self, image_api_address):
        self.image_api_address = image_api_address

    def metadata_for(self, image_id, language=None, width=None):
        try:
            url = "{}/image-api/v2/images/{}/imageUrl".format(self.image_api_address, image_id)
            response = requests.get(url, params={'language': language, 'width': width})
            response.raise_for_status()
            meta = response.json()
            return ImageMetaData(meta['id'], meta['url'], meta.get('alttext'))
        except Exception as e:
            logging.error("Could not get information about image. Received error %s", e, exc_info=1)
            return None




