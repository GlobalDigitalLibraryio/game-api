from boto3.dynamodb.conditions import Attr, Key

from models import Game, ValidationError


class GameRepository:

    def __init__(self, game_table):
        self.game_table = game_table

    def with_uuid(self, game_uuid):
        result = self.game_table.get_item(Key={'game_uuid': game_uuid})
        if result.get('Item'):
            return Game.to_api_structure(result['Item'])
        else:
            return None

    def with_external_id(self, external_id):
        response = self.game_table.query(
            IndexName='external_id-index',
            KeyConditionExpression=Key('external_id').eq(external_id))

        if len(response['Items']) > 0:
            return self.with_uuid(response['Items'][0]['game_uuid'])
        else:
            return None

    def all(self, page, page_size):
        data = self.game_table.scan()['Items']
        totalCount = len(data)
        if not page:
            page = 1
        if not page_size:
            page_size = 10

        start_index = page_size * (page - 1 )
        end_index = page_size * page
        data = data[start_index:end_index]
        return {
            "totalCount": totalCount,
            "page": page,
            "pageSize": page_size,
            "results": [Game.to_api_structure(x) for x in data]
        }

    def all_with_language(self, language):
        items = self.game_table.scan(FilterExpression=Attr('language').eq(language))
        return [Game.to_api_structure(x) for x in items['Items']]

    def add(self, game_json):
        to_add = Game.to_db_structure(game_json)
        if self.with_external_id(to_add['external_id']):
            raise ValidationError('Input payload validation failed', errors={
                'external_id': 'external_id {} already exists.'.format(to_add['external_id'])})

        self.game_table.put_item(Item=to_add)
        return Game.to_api_structure(to_add)

    def update(self, game_uuid, game_json):
        if not self.with_uuid(game_uuid):
            return None

        to_update = Game.to_db_structure(game_json)
        to_update['game_uuid'] = game_uuid

        self.game_table.put_item(Item=to_update)
        return Game.to_api_structure(to_update)

    def delete(self, game_uuid):
        self.game_table.delete_item(Key={'game_uuid': game_uuid})
