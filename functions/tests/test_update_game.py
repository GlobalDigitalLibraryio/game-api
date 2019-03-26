import unittest
from unittest.mock import Mock, patch

from gdl.update_game import UpdateGame


class UpdateGameTestCase(unittest.TestCase):
    input_as_output = lambda x: x

    def setUp(self):
        self.games_table_mock = Mock()
        self.update_game = UpdateGame(self.games_table_mock)

    @patch('gdl.update_game.not_found', side_effect=input_as_output)
    @patch('gdl.update_game.jsonify', side_effect=input_as_output)
    def test_that_update_non_existing_returns_not_found(self, jsonify_mock, not_found_mock):
        self.games_table_mock.get_item.return_value = {}
        assert self.update_game.main('does_not_exist', {}) == "Game with id does_not_exist was not found"

    @patch('gdl.update_game.jsonify', side_effect=input_as_output)
    def test_that_update_does_not_alter_id(self, jsonify_mock):
        game_uuid = '123-123-123-123'
        game = {
            'game_uuid': game_uuid,
            'external_id': 'external-id',
            'title': 'title',
            'description': 'description',
            'language': 'en-GB',
            'url': 'some-url',
            'license': 'some-license',
            'source': 'some-source',
            'publisher': 'some-publisher',
            'coverimage': 1
        }

        self.games_table_mock.get_item.return_value = {'Item': game}
        response = self.update_game.main(game_uuid, game)
        assert response['game_uuid'] == game_uuid


