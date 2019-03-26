import unittest
from unittest.mock import Mock, patch

from gdl.list_languages import ListLanguages


class ListLanguagesTestCase(unittest.TestCase):

    def setUp(self):
        self.games_table_mock = Mock()
        self.list_language = ListLanguages(self.games_table_mock)

    @patch('gdl.list_languages.jsonify', side_effect=lambda x: x)
    def test_that_languages_are_returned_with_description(self, jsonify_mock):
        items = {'Items': [{'language': 'nb'}, {'language': 'en-GB'}]}
        self.games_table_mock.scan.return_value = items

        result = self.list_language.main()
        assert len(result) == 2
        assert result[0]['code'] == 'nb'
        assert result[0]['description'] == 'Norwegian Bokmål'
        assert result[1]['code'] == 'en-GB'
        assert result[1]['description'] == 'English, United Kingdom'

    @patch('gdl.list_languages.jsonify', side_effect=lambda x: x)
    def test_that_empty_list_is_returned_when_no_entries(self, jsonify_mock):
        items = {'Items': []}
        self.games_table_mock.scan.return_value = items

        result = self.list_language.main()
        assert len(result) == 0


if __name__ == '__main__':
    unittest.main()

