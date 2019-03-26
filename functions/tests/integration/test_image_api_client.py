import unittest
from unittest.mock import patch

import requests_mock
from requests.exceptions import HTTPError

from gdl.integration.image_api_client import ImageApiClient


class ImageApiClientTestCase(unittest.TestCase):

    def setUp(self):
        self.image_api_client = ImageApiClient("http://mock-address")

    @requests_mock.mock()
    @patch('gdl.integration.image_api_client.logging')
    def test_that_none_is_returned_when_integration_error(self, req_mock, logging_mock):
        req_mock.get(requests_mock.ANY, exc=HTTPError("something happened"))
        assert self.image_api_client.metadata_for(image_id=1) is None
        self.assertTrue(logging_mock.error.called)

    @requests_mock.mock()
    def test_that_image_meta_is_returned(self, req_mock):
        req_mock.get(requests_mock.ANY, json={'id': 123, 'url': 'some-url', 'alttext': 'some-alttext'})
        response = self.image_api_client.metadata_for(image_id=1)
        self.assertEqual(123, response.id)
        self.assertEqual('some-url', response.url)
        self.assertEqual('some-alttext', response.alttext)
