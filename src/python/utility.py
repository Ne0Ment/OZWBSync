import json

DEFAULT_SETTINGS_PATH = 'settings.json'


def load_settings(settings_uri=DEFAULT_SETTINGS_PATH):
    with open(settings_uri, 'r') as f:
        vals = json.load(f)
        return Settings(vals['ozon_token']), vals['ozon_clientid'], vals['wb_token'], vals['ozon_token']


class Settings():
    def __init__(self, ozon_token=None, ozon_clientid=None, wb_token=None, db_uri=None) -> None:
        self.ozon_token = ozon_token
        self.ozon_clientid = ozon_clientid
        self.wb_token = wb_token
        self.db_uri = db_uri
