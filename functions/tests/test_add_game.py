import unittest
from unittest.mock import Mock, patch

from gdl.add_game import AddGame


class AddGameTestCase(unittest.TestCase):

    def setUp(self):
        self.games_table_mock = Mock()
        self.add_games = AddGame(self.games_table_mock)

    @patch('gdl.add_game.jsonify', side_effect=lambda x: x)
    def test_that_uuid_is_added_to_a_new_game_and_language_code_is_formatted(self, jsonify_mock):
        response = self.add_games.main({
            'external_id': 'external-id',
            'title': 'title',
            'description': 'description',
            'language': 'en-gb',
            'url': 'some-url',
            'license': 'some-license',
            'source': 'some-source',
            'publisher': 'some publisher',
            'coverimage': 1
        })

        assert response['game_uuid'] is not None
        assert response['language'] == 'en-GB'
