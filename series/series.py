import json
import asyncio
from core.common import BaseBuild
from core.utils import build_short_name
from core.exceptions import NonSingularResponseError
from graphQL import mutations, query
from .schema import POST_NEW_SERIES, POST_NEW_SERIES_TEAMS, UPDATE_SERIES_END_DATE, UPDATE_SERIES_START_DATE, \
    GET_ALL_SERIES_BY_NAME
from core.logger import Logger

logger = Logger.get_logger(__name__)


class Series(BaseBuild):

    @classmethod
    def exists(cls, **kwargs):
        name = kwargs.get('name')
        gender = kwargs.get('gender')
        pool = kwargs.get('pool')
        season = kwargs.get('season')

        result = asyncio.run(
            query.core_query({"name": name, 'gender': gender, "pool": pool, "season": season}, GET_ALL_SERIES_BY_NAME))
        series = result['series']

        if not series:
            return None
        if len(series) == 1:
            return series
        if len(series) > 1:
            raise NonSingularResponseError("Number of series with the given filter is more than 1.")

    @classmethod
    def build_data(cls, path, **kwargs):
        teams = [kwargs.get('team_a_id'), kwargs.get('team_b_id')]
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            series_name = obj['info']['event']['name']
            p = dict()
            p['name'] = "{}, {}".format(series_name, str(obj['info']['season']))
            p['short_name'] = build_short_name(series_name)
            p['gender'] = obj['info']['gender']
            p['pool'] = obj['info']['team_type']
            p['series_host_nations'] = None
            p['description'] = None
            p['series_teams'] = {
                'data': [
                    {
                        'team_id': teams[0]
                    },
                    {
                        'team_id': teams[1]
                    }
                ]
            }
            p['season'] = str(obj['info']['season'])
            p['start_date'] = obj['info']['dates'][0]
            p['end_date'] = obj['info']['dates'][-1]

        data = {'model': "series.Series", 'fields': p}
        return data

    @classmethod
    def mutate(cls, data, **kwargs):
        result = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_SERIES, data=data['fields']))

        try:
            ids = dict()
            ids['series'] = result['insert_series_one']['id']
            logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_SERIES", str(result)))
        except Exception as e:
            raise Exception(repr(e) + ' mutate function - series.series')

        return ids

    @classmethod
    def update(cls, data, **kwargs):
        series_id = kwargs.get('series')
        start_date_fields = {'series': series_id, 'start_date': data['fields']['start_date']}
        end_date_fields = {'series': series_id, 'end_date': data['fields']['end_date']}
        series_teams = [
            {
                'series_id': series_id,
                'team_id': kwargs.get('team_a_id')
            },
            {
                'series_id': series_id,
                'team_id': kwargs.get('team_b_id')
            }
        ]

        res_teams = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_SERIES_TEAMS, data=series_teams))
        logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_SERIES_TEAMS", str(res_teams)))
        res_start_date = asyncio.run(
            mutations.update_mutation(mutation_type=UPDATE_SERIES_START_DATE, data=start_date_fields))
        logger.info("Mutation<{}>:Status<success>:{}".format("UPDATE_SERIES_START_DATE", str(res_start_date)))
        res_end_date = asyncio.run(
            mutations.update_mutation(mutation_type=UPDATE_SERIES_END_DATE, data=end_date_fields))
        logger.info("Mutation<{}>:Status<success>:{}".format("UPDATE_SERIES_END_DATE", str(res_end_date)))
