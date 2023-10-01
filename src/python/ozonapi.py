from dbclasses import DBConnection
from ozonattributes import Attribute
from ozonproduct import OzonNDSValue, OzonProduct
import requests
import json
from typing import List
import logging

REQUEST_LIMIT = 1000
PRODUCT_LIST_URI = 'https://api-seller.ozon.ru/v2/product/list'
UPLOAD_PRODUCT_URI = 'https://api-seller.ozon.ru/v2/product/import'
DELETE_PRODUCTS_URI = 'https://api-seller.ozon.ru/v2/products/delete'
ARCHIVE_PRODUCTS_URI = 'https://api-seller.ozon.ru/v1/product/archive'
UPDATE_CHARACTERISTICS_URI = 'https://api-seller.ozon.ru/v1/product/attributes/update'
GET_ATTRIBUTES_URI = 'https://api-seller.ozon.ru/v3/products/info/attributes'
UPDATE_OFFER_IDS_URI = 'https://api-seller.ozon.ru/v1/product/update/offer-id'


class OzonApi():
    def __init__(self, client_id, api_key) -> None:
        self.client_id = client_id
        self.api_key = api_key
        self.headers = {
            'Client-Id': client_id,
            'Api-Key': api_key
        }
        self.verifier = DBConnection().init_verifier()

    def get_all_products(self, _filter={}):
        json_data = {
            'limit': REQUEST_LIMIT,
            'filter': _filter,
        }
        items = []
        last_id = None
        while True:
            r = requests.post(PRODUCT_LIST_URI,
                              headers=self.headers,
                              json=json_data if last_id is None else {**json_data, 'last_id': last_id})
            if r.status_code != 200:
                logging.error(r.status_code, r.text)
                return None

            parsed = json.loads(r.text)
            items += parsed['result']['items']
            if len(items) >= parsed['result']['total']:
                break
        return items

    def get_archived_products(self):
        return self.get_all_products({
            'visibility': 'ARCHIVED'
        })

    def get_products_attribs(self, offer_ids):
        json_data = {
            'limit': REQUEST_LIMIT,
            'filter': {
                'offer_id': offer_ids
            }
        }
        req = requests.post(GET_ATTRIBUTES_URI,
                            headers=self.headers,
                            json=json_data)

        if req.status_code != 200:
            logging.error(req.status_code, req.text)
            return

        return json.loads(req.text)['result']

    def update_attributes(self, offer_ids, attributes):
        attributes_json = [self._form_attrib_request(attrib)
                           for attrib in attributes]
        json_data = {
            'items': [{
                'offer_id': offer_id,
                'attributes': attributes_json
            } for offer_id in offer_ids]
        }
        req = requests.post(UPDATE_CHARACTERISTICS_URI,
                            headers=self.headers,
                            json=json_data)
        if req.status_code != 200:
            logging.error(req.status_code, req.text)

    def update_offer_ids(self, update_offer_ids):
        req = requests.post(UPDATE_OFFER_IDS_URI,
                            headers=self.headers,
                            json={
                                'update_offer_id': update_offer_ids
                            })
        if req.status_code != 200:
            logging.error(req.status_code, req.text)

    def upload_products(self, products: List[OzonProduct]):
        json_data = {
            'items': []
        }
        for product in products:
            json_data['items'].append(self._form_creation_request(product))
        r = requests.post(UPLOAD_PRODUCT_URI,
                          headers=self.headers,
                          json=json_data)
        if r.status_code != 200:
            logging.error(r.status_code, r.text)
        return r.status_code

    def _form_creation_request(self, product: OzonProduct):
        return {
            'offer_id': product.info.offer_id,
            'category_id': product.info.category_id,
            'currency_code': 'RUB',
            'images': product.media.images,
            'name': product.info.name,
            'dimension_unit': product.dimensions.dimension_unit.value,
            'depth': product.dimensions.depth,
            'height': product.dimensions.height,
            'width': product.dimensions.width,
            'price': str(product.price.price),
            'old_price': str(product.price.old_price),
            'vat': OzonNDSValue.ZERO.value,
            'weight': product.weight.weight,
            'weight_unit': product.weight.weight_unit.value,
            'attributes': [self._form_attrib_request(attrib) for attrib in product.attributes]
        }

    def _form_attrib_request(self, attrib: Attribute):
        d = {
            'complex_id': 0,
            'id': attrib._id,
            'values': []
        }
        if type(attrib.value) != list:
            d['values'] = [self._form_attrib_value_request(
                attrib.value, attrib._id)]
        else:
            d['values'] = [self._form_attrib_value_request(
                val, attrib._id) for val in attrib.value]
        return d

    def _form_attrib_value_request(self, attrib_value, attrib_id):
        return {
            'dictionary_value_id': self.verifier._get_value_id(attrib_id, attrib_value),
            'value': str(attrib_value)
        }

    def archive(self, what_to_archive):
        products = [p for p in self.get_all_products() if what_to_archive(p)]
        product_chunks = [products[x:x+100]
                          for x in range(0, len(products), 100)]
        for chunk in product_chunks:
            json_data = {
                'product_id': [p['product_id'] for p in chunk]
            }
            req = requests.post(ARCHIVE_PRODUCTS_URI,
                                headers=self.headers,
                                json=json_data)
            if req.status_code != 200:
                logging.error(req.status_code, req.text)

    def delete(self, what_to_delete):
        products = [p for p in self.get_all_products() if what_to_delete(p)]
        product_chunks = [products[x:x+100]
                          for x in range(0, len(products), 100)]
        for chunk in product_chunks:
            json_data = {
                'product_id': [p['product_id'] for p in chunk]
            }
            req = requests.post(DELETE_PRODUCTS_URI,
                                headers=self.headers,
                                json=json_data)
            if req.status_code != 200:
                logging.error(req.status_code, req.text)
