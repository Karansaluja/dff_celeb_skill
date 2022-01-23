from custom_exceptions import exceptions


class Config:
    def __init__(self):
        self.config_map = {"mongo_address": "mongodb://localhost:27017/"}

    def get_config_value(self, key: str):
        val = self.config_map.get(key)
        if val is not None:
            return val
        raise exceptions.ConfigNotFoundException("No such key in config map")