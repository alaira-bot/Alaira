import warnings
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig import YamlDataClassConfig

CONFIG = None


@dataclass
class _AlairaDatabaseConfig(DataClassJsonMixin):
    port: int = None


@dataclass
class _AlairaBotConfig(DataClassJsonMixin):
    token: str = None


@dataclass
class AlairaConfig(YamlDataClassConfig):
    database: _AlairaDatabaseConfig = None
    bot: _AlairaBotConfig = None


class AlairaConfigLoader:
    @staticmethod
    def load(path: str) -> AlairaConfig:
        global CONFIG
        if CONFIG:
            return CONFIG
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            config = AlairaConfig()
            config.load(path)
            CONFIG = config
            return config

    @staticmethod
    def get_current() -> AlairaConfig:
        return CONFIG

    @staticmethod
    def reload(path: str) -> AlairaConfig:
        global CONFIG
        CONFIG = None
        return AlairaConfigLoader.load(path)
