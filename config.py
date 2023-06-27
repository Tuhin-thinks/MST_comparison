import json
from typing import Union, Any
from pathlib import Path


class ConfigSingleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigSingleton, cls).__new__(cls)
        return cls.instance

    def set_config_filepath(self, config_filepath: Union[str, Path]):
        self.config_filepath = Path(config_filepath)
        self.config = self.read_config()

    def read_config(self):
        with open(self.config_filepath, 'r') as f:
            config = json.load(f)
        return config

    def get_config(self, key: str):
        return self.config[key]

    def __getattr__(self, item: str):
        try:
            return self.config[item]
        except KeyError:
            raise KeyError(f"Key {item} not found in config file.")


if __name__ == '__main__':
    # demonstration of singleton usage of this class

    # declare the instance of the singleton class
    c1 = ConfigSingleton()
    c1.set_config_filepath(Path(__file__).parent.joinpath("config.json"))

    # get the config value
    c2 = ConfigSingleton()
    print(c2.config_filepath)
    print("N_DECIMALS:", c2.N_DECIMALS)

    print("Setting N_DECIMALS to 5")
    c2.N_DECIMALS = 5

    print("N_DECIMALS:", c2.N_DECIMALS)

    # print("Accessing non-existent key:", c2.NON_EXISTENT_KEY)

    print("Setting 'NEW_KEY' key to 5")
    c2.NEW_KEY = 5

    print("Accessing 'NEW_KEY' key:", c2.NEW_KEY)
