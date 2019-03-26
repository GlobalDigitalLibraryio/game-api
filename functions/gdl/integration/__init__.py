class ImageMetaData:
    def __init__(self, id, image_url, alttext=None):
        self.__id = id
        self.__image_url = image_url
        self.__alttext = alttext

    @property
    def id(self):
        return self.__id

    @property
    def url(self):
        return self.__image_url

    @property
    def alttext(self):
        return self.__alttext

    def as_dict(self):
        image_dict = {
            'url': self.url,
            'imageId': self.id
        }
        if self.alttext:
            image_dict['alttext'] = self.alttext

        return image_dict
