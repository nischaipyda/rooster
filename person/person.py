from core.parser import BaseParser
from core.mixins import MutateMixins
from graphQL.mutations import bulk_mutation
from .schema import BULK_POST_NEW_PERSON

from settings import PERSON_DIR
from core.logger import Logger

logger = Logger.get_logger(__name__)


class Person(BaseParser):
    class Meta:
        input_file_path = PERSON_DIR / "people.csv"
        output_file_name = "person.json"

    @classmethod
    def build_data(cls, **kwargs):
        temp_file_name = cls._meta.input_file_path.resolve().parent / "temp" / "person.csv"
        if cls._meta.input_file_path.suffix == '.csv' or temp_file_name.suffix == '.csv':
            import csv
            with open(temp_file_name, 'r') as inf:
                data = csv.DictReader(inf)
                people = []
                for row in data:
                    row = {key: (None if value == "" else value) for key, value in row.items()}
                    people.append(row)
            return people

    @classmethod
    def mutate(cls):
        result = MutateMixins.bulk_mutate(bulk_mutation, mutation_type=BULK_POST_NEW_PERSON,
                                          file=cls._get_bake_file_path())
        logger.info("BulkMutation<{}>:Status<success>:{}".format("BULK_POST_NEW_PERSON", str(result)))
