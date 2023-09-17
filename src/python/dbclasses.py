from pymongo.mongo_client import MongoClient


class DBConnection():
    def __init__(self, db_uri=None) -> None:
        self.uri = db_uri
        self.client: MongoClient = MongoClient(self.uri)

    def test_connection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False
