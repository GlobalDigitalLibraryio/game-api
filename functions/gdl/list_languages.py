from flask import jsonify
from language_tags import tags


class ListLanguages():
    def __init__(self, games_table):
        self.games_table = games_table

    def main(self):
        languages = [{'code': x['language'], 'description': ', '.join(tags.description(x['language']))} for x in
                     self.games_table.scan()['Items']]
        return jsonify(languages)
