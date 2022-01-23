from custom_exceptions import exceptions

config_map = {"mongo_address": "mongodb://localhost:27017/"}


def get_config_value(key: str):
    val = config_map.get(key)
    if val is not None:
        return val
    raise exceptions.ConfigNotFoundException("No such key in config map")
