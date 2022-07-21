import json
import asyncio

from core.common import BaseBuild
from core.exceptions import NonSingularResponseError
from graphQL import query, mutations
from .schema import (
    GET_ALL_GROUPS_BY_TOURNAMENT,
    GET_ALL_TOURNAMENTS_BY_SERIES_AND_FORMAT,
    GET_GROUPS_TEAMS_COUNT_BY_TOURNAMENT,
    POST_NEW_TOURNAMENT,
    POST_NEW_GROUP,
    POST_NEW_GROUP_TEAMS,
    UPDATE_TOURNAMENT_START_DATE,
    UPDATE_TOURNAMENT_END_DATE,
    UPDATE_TOURNAMENT_GROUPS_AND_TEAMS_COUNT,
)
from core.logger import Logger

logger = Logger.get_logger(__name__)


class Tournament(BaseBuild):

    @classmethod
    def exists(cls, **kwargs):
        series_id = kwargs.get('series_id')
        tournament_format = kwargs.get('format')
        result = asyncio.run(query.core_query({"series": series_id, 'format': tournament_format},
                                              GET_ALL_TOURNAMENTS_BY_SERIES_AND_FORMAT))
        tournament = result['tournament']
        if not tournament:
            return None
        if len(tournament) == 1:
            return tournament
        if len(tournament) > 1:
            raise NonSingularResponseError("Number of tournaments with the given filter is more than 1.")

    @classmethod
    def build_data(cls, path, **kwargs):
        series_id = kwargs.get('series')
        model = 'tournament.Tournament'
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            p = dict({})
            p['series_id'] = series_id
            p['format'] = obj['info']['match_type']
            p['start_date'] = obj['info']['dates'][0]
            p['end_date'] = obj['info']['dates'][-1]
            p['trophy_id'] = None
            p['balls_per_over'] = obj['info']['balls_per_over']
            p['status'] = "COMPLETED"
            p['teams_count'] = None
            p['groups_count'] = None
            p['group_size'] = None
            p['group_qualify_size'] = None
            p['win_points'] = None
            p['nr_points'] = None
            p['loss_points'] = None

        return {'model': model, 'fields': p}

    @classmethod
    def mutate(cls, data, **kwargs):
        result = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_TOURNAMENT, data=data['fields']))

        try:
            ids = dict()
            ids['tournament'] = result['insert_tournament_one']['id']
            logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_TOURNAMENT", str(result)))
        except Exception as e:
            raise Exception(repr(e) + ' mutate function - tournament.Tournament')

        return ids

    @classmethod
    def update(cls, data, **kwargs):
        tournament_id = kwargs.get('tournament')
        start_date_fields = {'tournament': tournament_id, 'start_date': data['fields']['start_date']}
        end_date_fields = {'tournament': tournament_id, 'end_date': data['fields']['end_date']}

        res_start_date = asyncio.run(
            mutations.update_mutation(mutation_type=UPDATE_TOURNAMENT_START_DATE, data=start_date_fields))
        logger.info("Mutation<{}>:Status<success>:{}".format("UPDATE_TOURNAMENT_START_DATE", str(res_start_date)))
        res_end_date = asyncio.run(
            mutations.update_mutation(mutation_type=UPDATE_TOURNAMENT_END_DATE, data=end_date_fields))
        logger.info("Mutation<{}>:Status<success>:{}".format("UPDATE_TOURNAMENT_START_DATE", str(res_end_date)))


class Group(BaseBuild):
    @classmethod
    def exists(cls, **kwargs):
        tournament_id = kwargs.get('tournament_id')
        group_name = kwargs.get('name')
        result = asyncio.run(
            query.core_query({'tournament': tournament_id, 'name': group_name}, GET_ALL_GROUPS_BY_TOURNAMENT))
        group = result['group']
        if not group:
            return None
        if len(group) == 1:
            return group
        if len(group) > 1:
            raise NonSingularResponseError("Number of groups with the given filter is more than 1.")

    @classmethod
    def build_data(cls, path, **kwargs):
        tournament_id = kwargs.get('tournament')
        teams = [kwargs.get('team_a_id'), kwargs.get('team_b_id')]

        model = "tournament.Group"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            p = dict({})
            try:
                p['tournament_id'] = tournament_id
                p['group_teams'] = {
                    'data': [
                        {
                            'team_id': teams[0]
                        },
                        {
                            'team_id': teams[1]
                        }
                    ]
                }
                p['name'] = obj['info']['event']['group']
            except KeyError:
                p['name'] = 'default'

            data = {'model': model, 'fields': p}
            return data

    @classmethod
    def mutate(cls, data, **kwargs):
        result = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_GROUP, data=data['fields']))
        try:
            ids = dict()
            ids['group'] = result['insert_group_one']['id']
            logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_GROUP", str(result)))
        except Exception as e:
            raise Exception(repr(e) + ' mutate function - tournament.Tournament')

        return ids

    @classmethod
    def update(cls, data, **kwargs):
        tournament_id = kwargs.get('tournament')
        group_id = kwargs.get('group')
        group_teams = [
            {
                'group_id': group_id,
                'team_id': kwargs.get('team_a_id')
            },
            {
                'group_id': group_id,
                'team_id': kwargs.get('team_b_id')
            }
        ]
        res_groups = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_GROUP_TEAMS, data=group_teams))
        logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_GROUP_TEAMS", str(res_groups)))

        counts = asyncio.run(query.core_query({'tournament': tournament_id}, GET_GROUPS_TEAMS_COUNT_BY_TOURNAMENT))
        update_counts = {
            'tournament': tournament_id,
            'groups_count': counts['group_aggregate']['aggregate']['count'],
            'teams_count': counts['group_teams_aggregate']['aggregate']['count']
        }

        res_counts = asyncio.run(
            mutations.update_mutation(mutation_type=UPDATE_TOURNAMENT_GROUPS_AND_TEAMS_COUNT, data=update_counts))
        logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_GROUP_TEAMS", str(res_counts)))
