import requests
import json

PRODUCT_LIST_URI = 'https://api-seller.ozon.ru/v2/product/list'
REQUEST_LIMIT = 1000


class OzonApi():
    def __init__(self, client_id, api_key) -> None:
        self.client_id = client_id
        self.api_key = api_key
        self.headers = {
            'Client-Id': client_id,
            'Api-Key': api_key
        }

    def get_all_products(self):
        json_data = {
            'limit': REQUEST_LIMIT,
            'filter': {},
        }
        items = []
        last_id = None
        while True:
            r = requests.post(PRODUCT_LIST_URI,
                              json=json_data if last_id is None else {**json_data, 'last_id': last_id})
            if r.status_code != 200:
                print(r.status_code, r.text)
                return None

            parsed = json.loads(r.text)
            items += parsed['items']
            if len(items) >= parsed['total']:
                break
        return items
