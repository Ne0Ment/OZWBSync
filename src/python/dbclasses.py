from pymongo.mongo_client import MongoClient

from python.ozonproduct import OzonProductCategory
from python.serializers import OzonAttributeSerializer, OzonAttributeVerifier, OzonGeneralProductSerializer, OzonProductCategorySerializer

DEFAULT_DB_URI = 'mongodb://localhost:27017'
DEFAULT_DB_NAME = 'OZWBSync'
PRODUCT_CATEGORIES_COLLECTION_NAME = 'product-categories'
OZON_ATTRIBUTE_VERIFIER_PATH = 'ms_attrib_dict.pickle'


class DBConnection():
    """
     - load all ProductCaterogires
     - load ProductCategory
     - update ProductCategory
    """

    def __init__(self, db_uri=DEFAULT_DB_URI, db_name=DEFAULT_DB_NAME) -> None:
        self.uri = db_uri
        self.client: MongoClient = MongoClient(self.uri)
        self.db_name = db_name
        self.db = self.client[db_name]
        self.product_categories = self.db[PRODUCT_CATEGORIES_COLLECTION_NAME]
        self.attribute_serializer = OzonAttributeSerializer(
            OzonAttributeVerifier(OZON_ATTRIBUTE_VERIFIER_PATH))
        self.product_serializer = OzonGeneralProductSerializer(
            self.attribute_serializer)
        self.category_serializer = OzonProductCategorySerializer(
            self.product_serializer)

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
