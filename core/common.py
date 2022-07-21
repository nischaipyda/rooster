from settings import MATCHES_DIR
from abc import abstractmethod
import os


def get_file_name():
    for file in os.listdir(MATCHES_DIR):
        if os.path.isfile(MATCHES_DIR / file) and file.split(".")[1] == "json":
            yield file


class MatchFilePath:
    input = MATCHES_DIR / "64071.json"
    output = "64071.json"


class BaseBuild:

    @classmethod
    def exists(cls, **kwargs):
        return None

    @classmethod
    @abstractmethod
    def build_data(cls, path):
        pass

    @classmethod
    def mutate(cls, data, **kwargs):
        pass
