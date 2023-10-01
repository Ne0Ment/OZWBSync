from logistics import CategoryStock
from pymongo.mongo_client import MongoClient

from ozonproduct import OzonProductCategory
from serializers import CategoryStockSerializer, OzonAttributeSerializer, OzonAttributeVerifier, OzonGeneralProductSerializer, OzonProductCategorySerializer

DEFAULT_DB_URI = 'mongodb://localhost:27017'
DEFAULT_DB_NAME = 'OZWBSync'
PRODUCT_CATEGORIES_COLLECTION_NAME = 'product-categories'
OZON_DICT_COLLECTION_NAME = 'ozon-dicts'
STOCK_COLLECTION_NAME = 'product-stocks'


class DBConnection():
    def __init__(self, db_uri=DEFAULT_DB_URI, db_name=DEFAULT_DB_NAME) -> None:
        self.uri = db_uri
        self.client: MongoClient = MongoClient(self.uri)
        self.db_name = db_name
        self.db = self.client[db_name]
        self.product_categories = self.db[PRODUCT_CATEGORIES_COLLECTION_NAME]
        self.ozon_dicts = self.db[OZON_DICT_COLLECTION_NAME]
        self.stocks = self.db[STOCK_COLLECTION_NAME]
        self.attribute_serializer = OzonAttributeSerializer(
            self.init_verifier())
        self.product_serializer = OzonGeneralProductSerializer(
            self.attribute_serializer)
        self.category_serializer = OzonProductCategorySerializer(
            self.product_serializer)
        self.category_stock_serializer = CategoryStockSerializer()

    def test_connection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False

    def load_product_categories(self):
        return [self.category_serializer.deserialize(i) for i in self.product_categories.find({})]

    def load_product_category(self, categury_name):
        return self.category_serializer.deserialize(self.product_categories.find_one({'category_name': categury_name}))

    def save_product_category(self, category: OzonProductCategory):
        return self.product_categories.replace_one({'category_name': category.category_name},
                                                   self.category_serializer.serialize(
                                                       category),
                                                   upsert=True)

    def clear_db(self):
        self.client.drop_database(self.db_name)

    def upload_ozon_dicts(self, ozon_dicts):
        inserted_id = self.ozon_dicts.insert_one(ozon_dicts).inserted_id
        self.ozon_dicts.delete_many({'_id': {'$ne': inserted_id}})

    def get_ozon_dicts(self):
        return self.ozon_dicts.find_one()

    def init_verifier(self):
        return OzonAttributeVerifier(dict((int(key) if key != '_id' else -1, value) for (key, value) in self.get_ozon_dicts().items()))

    def save_category_stock(self, stock: CategoryStock):
        self.stocks.replace_one({'category_name': stock.category_name},
                                self.category_stock_serializer(stock),
                                upsert=True)

    def get_category_stock(self, category_name):
        return self.stocks.find_one({'category_name': category_name})
