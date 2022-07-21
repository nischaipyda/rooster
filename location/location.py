import json
import asyncio
from core.utils import convert_id_suffix_key_to_base64
from core.parser import BaseParser
from core.mixins import MutateMixins
from core.common import BaseBuild
from core.logger import Logger
from settings import LOCATION_DIR
from .schema import BULK_POST_NEW_STATE, BULK_POST_NEW_CITY, BULK_POST_NEW_COUNTRY, POST_NEW_VENUE, GET_VENUE_BY_NAME
from graphQL import mutations, query
from core.exceptions import NonSingularResponseError
from .utils import get_city_by_name

logger = Logger.get_logger(__name__)


class Country(BaseParser):
    class Meta:
        input_file_path = LOCATION_DIR / "countries.json"
        output_file_name = "countries.json"
        delete_fields = ['timezones', 'translations', 'native', 'emojiU']

    @classmethod
    def mutate(cls):
        MutateMixins.bulk_mutate(mutations.bulk_mutation, mutation_type=BULK_POST_NEW_COUNTRY,
                                 file=cls._get_bake_file_path())


class State(BaseParser):
    class Meta:
        input_file_path = LOCATION_DIR / "states.json"
        output_file_name = "states.json"
        delete_fields = ['country_code', 'country_name']

    @classmethod
    def mutate(cls):
        MutateMixins.bulk_mutate(mutations.bulk_mutation, mutation_type=BULK_POST_NEW_STATE,
                                 file=cls._get_bake_file_path())


class City(BaseParser):
    class Meta:
        input_file_path = LOCATION_DIR / "cities.json"
        output_file_name = "cities.json"
        delete_fields = ['state_code', 'state_name', 'country_code', 'country_name', 'wikiDataId']

    @classmethod
    def mutate(cls):
        MutateMixins.bulk_mutate(mutations.bulk_mutation, mutation_type=BULK_POST_NEW_CITY, file=cls._get_bake_file_path())


class Venue(BaseBuild):

    @classmethod
    def exists(cls, **kwargs):
        name = kwargs.get('name')

        result = asyncio.run(query.core_query({"name": name}, GET_VENUE_BY_NAME))
        venues = result['venue']

        if venues is None:
            return None
        if len(venues) == 1:
            return venues
        if len(venues) > 1:
            raise NonSingularResponseError("Number of series with the given filter is more than 1.")

    @classmethod
    def build_data(cls, path, **kwargs):
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            p = dict()
            try:
                res = cls.exists(name=obj['info']['venue'])
                if res:
                    return {'model': "location.Venue", 'fields': {'id': res[0]['id']}}
                else:
                    p['name'] = obj['info']['venue']
            except KeyError:
                return None
            p['city_id'] = None
            p['state_id'] = None
            p['country_id'] = None

            data = {'model': "location.Venue", 'fields': p}

            return data

    @classmethod
    def mutate(cls, data, **kwargs):
        result = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_VENUE, data=data['fields']))

        try:
            ids = dict()
            ids['venue'] = result['venueCreate']['venue']['id']
            logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_VENUE", str(result)))
        except Exception as e:
            raise Exception(repr(e) + ' mutate function - location.Venue')

        return ids
