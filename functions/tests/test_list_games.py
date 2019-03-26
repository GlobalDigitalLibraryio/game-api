import unittest
from unittest.mock import Mock, patch

from gdl.integration import ImageMetaData
from gdl.list_games import ListGames


class ListGamesTestCase(unittest.TestCase):

    def setUp(self):
        self.games_table_mock = Mock()
        self.image_api_mock = Mock()
        self.list_games = ListGames(self.games_table_mock, self.image_api_mock)

    @patch('gdl.list_games.jsonify', side_effect=lambda x: x)
    def test_that_empty_list_is_returned_when_no_games(self, jsonify_mock):
        request = Mock()
        request.args = {}

        self.games_table_mock.scan.return_value = {'Items': []}
        assert self.list_games.main(request) == []

    @patch('gdl.list_games.jsonify', side_effect=lambda x: x)
    def test_that_all_games_returned_as_list(self, jsonify_mock):
        request = Mock()
        request.args = {}

        self.image_api_mock.metadata_for.side_effect = [
            ImageMetaData(1, "url", "alttext"),
            ImageMetaData(2, "url", "alttext")]

        items = {'Items': [{
            'game_uuid': 'uuid-1',
            'external_id': 'external_id-1',
            'title': 'title-1',
            'description': 'description-1',
            'language': 'nb',
            'url': 'url-1',
            'license': 'license-1',
            'source': 'source-1',
            'publisher': 'publisher-1',
            'coverimage': 1
        },{
            'game_uuid': 'uuid-2',
            'external_id': 'external_id-2',
            'title': 'title-2',
            'description': 'description-2',
            'language': 'nb',
            'url': 'url-2',
            'license': 'license-2',
            'source': 'source-2',
            'publisher': 'publisher-2',
            'coverimage': 2
        }]}

        self.games_table_mock.scan.return_value = items
        response = self.list_games.main(request)

        assert response[0]['game_uuid'] == 'uuid-1'
        assert response[1]['game_uuid'] == 'uuid-2'
        assert response[0]['coverimage']['imageId'] == 1
        assert response[1]['coverimage']['imageId'] == 2
