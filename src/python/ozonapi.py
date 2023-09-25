from ozonproduct import OzonNDSValue, OzonProduct
import requests
import json
from types import List

PRODUCT_LIST_URI = 'https://api-seller.ozon.ru/v2/product/list'
UPLOAD_PRODUCT_URI = 'https://api-seller.ozon.ru/v2/product/import'
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
                              headers=self.headers,
                              json=json_data if last_id is None else {**json_data, 'last_id': last_id})
            if r.status_code != 200:
                print(r.status_code, r.text)
                return None

            parsed = json.loads(r.text)
            items += parsed['result']['items']
            if len(items) >= parsed['result']['total']:
                break
        return items

    def upload_products(self, products: List[OzonProduct]):
        json_data = {
            'items': []
        }
        return json_data

    def _form_creation_request(product: OzonProduct):
        return {
            'category_id': product.info.category_id,
            'currency_code': 'RUB',
            'images': product.media.images,
            'name': product.info.name,
            'dimension_unit': product.dimensions.dimension_unit.value,
            'depth': product.dimensions.depth,
            'height': product.dimensions.height,
            'width': product.dimensions.width,
            'price': product.price.price,
            'old_price': product.price.old_price,
            'vat': OzonNDSValue.ZERO.value,
            'attributes': [{
                'a': attrib
            } for attrib in product.attributes]
        }
