from . import no_content

class DeleteGame:

    def __init__(self, games_table):
        self.games_table = games_table

    def main(self, game_uuid):
        self.games_table.delete_item(
            Key={
                'game_uuid': game_uuid
            }
        )

        return no_content()