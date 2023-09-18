import json

DEFAULT_SETTINGS_PATH = 'settings.json'


def load_settings(settings_uri=DEFAULT_SETTINGS_PATH):
    with open(settings_uri, 'r') as f:
        vals = json.load(f)
        return Settings(vals['ozon_token']), vals['ozon_clientid'], vals['wb_token'], vals['db_uri']


class Settings():
    def __init__(self, ozon_token=None, ozon_clientid=None, wb_token=None, db_uri=None) -> None:
        self.ozon_token = ozon_token
        self.ozon_clientid = ozon_clientid
        self.wb_token = wb_token
        self.db_uri = db_uri


def same_class(func):
    def wrapper(*args):
        if (args[0].__class__.__qualname__ != args[1].__class__.__qualname__):
            return False
        return func(*args)
    return wrapper
