from pymongo.mongo_client import MongoClient

DEFAULT_DB_URI = 'mongodb://localhost:27017'
DEFAULT_DB_NAME = 'OZWBSync'
PRODUCT_CATEGORIES_COLLECTION_NAME = 'product-categories'


class DBConnection():
    """
     - load all ProductCaterogires
     - load ProductCategory
     - update ProductCategory
    """

    def __init__(self, db_uri=None, db_name=DEFAULT_DB_NAME) -> None:
        self.uri = db_uri
        self.client: MongoClient = MongoClient(self.uri)
        self.db = self.client[DEFAULT_DB_NAME]
        self.product_categories = self.db[PRODUCT_CATEGORIES_COLLECTION_NAME]

    def test_connection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False

    def load_productcategories(self):
        return self.client
