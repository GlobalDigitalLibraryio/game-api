import unittest
from unittest.mock import Mock, patch

from gdl.get_game import GetGame
from gdl.integration import ImageMetaData


class GetGameTestCase(unittest.TestCase):
    input_as_output = lambda x: x

    def setUp(self):
        self.games_table_mock = Mock()
        self.image_api_mock = Mock()
        self.get_game = GetGame(self.games_table_mock, self.image_api_mock)

    @staticmethod
    def same_value(message):
        return message

    @patch('gdl.get_game.not_found', side_effect=input_as_output)
    @patch('gdl.get_game.jsonify', side_effect=input_as_output)
    def test_that_not_found_is_returned_for_non_existing_id(self, get_game_mock, jsonify_mock):
        self.games_table_mock.get_item.return_value = {}
        assert self.get_game.main('does_not_exist') == "Game with id does_not_exist was not found"

    @patch('gdl.get_game.not_found', side_effect=input_as_output)
    @patch('gdl.get_game.jsonify', side_effect=input_as_output)
    def test_that_game_is_returned_for_valid_id(self, get_game_mock, jsonify_mock):
        self.image_api_mock.metadata_for.return_value = ImageMetaData(1, "url", "alttext")
        self.games_table_mock.get_item.return_value = {'Item': {
            'game_uuid': 'uuid',
            'external_id': 'external_id',
            'title': 'title',
            'description': 'description',
            'language': 'nb',
            'url': 'url',
            'license': 'license',
            'source': 'source',
            'publisher': 'publisher',
            'coverimage': 1
        }}

        result = self.get_game.main('uuid')
        assert result['game_uuid'] == 'uuid'
        assert result['coverimage']['imageId'] == 1
        assert result['coverimage']['url'] == 'url'
        assert result['coverimage']['alttext'] == 'alttext'

    @patch('gdl.get_game.not_found', side_effect=input_as_output)
    @patch('gdl.get_game.jsonify', side_effect=input_as_output)
    def test_that_game_is_returned_for_valid_id_even_if_cover_image_is_not_found(self, get_game_mock, jsonify_mock):
        self.image_api_mock.metadata_for.return_value = None
        self.games_table_mock.get_item.return_value = {'Item': {
            'game_uuid': 'uuid',
            'external_id': 'external_id',
            'title': 'title',
            'description': 'description',
            'language': 'nb',
            'url': 'url',
            'license': 'license',
            'source': 'source',
            'publisher': 'publisher',
            'coverimage': 1
        }}

        result = self.get_game.main('uuid')
        assert result['game_uuid'] == 'uuid'
        assert result.get('coverimage') is None

