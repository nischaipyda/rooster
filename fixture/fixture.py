import json
import asyncio
from graphQL import mutations, query
from core.common import BaseBuild
from .schema import POST_NEW_FIXTURE, GET_FIXTURE_BY_ID, GET_STAGE_BY_NAME
from core.exceptions import NonSingularResponseError
from core.logger import Logger

logger = Logger.get_logger(__name__)


def get_stage_id(name):
    result = asyncio.run(query.core_query({"name": name}, GET_STAGE_BY_NAME))
    stage = result['insert_stage']['returning']
    if not stage:
        return None
    if len(stage) == 1:
        return stage[0]['id']
    if len(stage) > 1:
        raise NonSingularResponseError("Number of stages with the given filter is more than 1.")


class Fixture(BaseBuild):

    @classmethod
    def exists(cls, **kwargs):
        fixture_id = kwargs.get('id')

        result = asyncio.run(query.query_by_id({"id": fixture_id}, GET_FIXTURE_BY_ID))
        fixture = result['fixture_by_pk']
        if fixture is None:
            return None
        if fixture_id == fixture['id']:
            try:
                ids = dict()
                ids['fixture'] = fixture['id']
                ids['outcome'] = fixture['outcome']['id']
                ids['toss'] = fixture['toss']['id']
                ids['versus'] = fixture['versus']['id']

                for i, ele in enumerate(fixture['innings']):
                    key = 'innings_' + str(i + 1)
                    ids[key] = ele['id']
            except KeyError as e:
                raise Exception(repr(e) + ' exists function - fixture.fixture')

            return ids

    @classmethod
    def build_data(cls, path, **kwargs):
        tournament_id = kwargs.get('tournament')
        fixture_data = kwargs.get('fixture')
        outcome = {'data': fixture_data['outcome']}
        venue = {'data': fixture_data['venue']}
        toss = {'data': fixture_data['toss']}
        fixture_officials = {'data': fixture_data['fixture_officials']}
        playing_xi = {'data': fixture_data['playing_xi']}
        innings = {'data': fixture_data['innings']}
        model = "fixture.Fixture"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)

            registry = obj['info']['registry']

            p = dict({})
            p['id'] = int(json_file.name.split('/')[-1].split('.')[0])
            p['tournament_id'] = tournament_id
            p['start_date'] = obj['info']['dates'][0]
            p['end_date'] = obj['info']['dates'][-1]
            p['neutral_venue'] = False
            p['outcome'] = outcome
            p['innings'] = innings
            p['versus'] = {
                'data': {
                    'fixture_id': p['id'],
                    'team_a_id': kwargs.get('team_a_id'),
                    'team_b_id': kwargs.get('team_b_id')
                }
            }
            p['toss'] = toss
            p['fixture_playing_xis'] = playing_xi
            p['fixture_officials'] = fixture_officials

            try:
                p['venue_id'] = venue['data']['id']
            except KeyError:
                p['venue'] = venue

            try:
                stg = get_stage_id(obj['info']['event']['stage'])
                if stg is None:
                    p['stage'] = {'data': {'name': obj['info']['event']['stage']}}
            except KeyError:
                p['stage'] = None

            try:
                p['fixture_players_of_match'] = {
                    'data': [
                        {'player_of_match_id': registry['people'][player]} for player in obj['info']['player_of_match']
                    ]
                }
            except KeyError:
                p['fixture_players_of_match'] = None

            try:
                p['match_number'] = obj['info']['event']['match_number']
            except KeyError:
                p['match_number'] = None

            data = {'model': model, 'fields': p}
            return data

    @classmethod
    def mutate(cls, data, **kwargs):
        result = asyncio.run(mutations.core_mutation(mutation_type=POST_NEW_FIXTURE, data=data['fields']))

        try:
            ids = dict()
            ids['fixture'] = result['insert_fixture_one']['id']
            ids['outcome'] = result['insert_fixture_one']['outcome']['id']
            ids['toss'] = result['insert_fixture_one']['toss']['id']
            ids['versus'] = result['insert_fixture_one']['versus']['id']

            for i, ele in enumerate(result['insert_fixture_one']['innings']):
                key = 'innings_' + str(i + 1)
                ids[key] = ele['id']

            logger.info("Mutation<{}>:Status<success>:{}".format("POST_NEW_SERIES", str(result)))
        except Exception as e:
            raise Exception(repr(e) + ' mutate function - fixture.fixture')

        return ids


class Innings(BaseBuild):
    @classmethod
    def build_data(cls, path, **kwargs):
        model = "fixture.Innings"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            innings = list()

            for i, ele in enumerate(obj['innings']):
                p = dict({})
                p['innings_number'] = i + 1
                p['team_batting_id'] = kwargs.get(obj['innings'][i]['team'])
                p['team_bowling_id'] = next(
                    kwargs.get(team) for team in obj['info']['teams'] if team != obj['innings'][i]['team'])

                try:
                    p['penalty_runs_pre_innings'] = obj['innings'][i]['penalty_runs']['pre']
                except KeyError:
                    p['penalty_runs_pre_innings'] = 0
                except Exception as e:
                    print(repr(e))

                try:
                    p['penalty_runs_post_innings'] = obj['innings'][i]['penalty_runs']['post']
                except KeyError:
                    p['penalty_runs_post_innings'] = 0

                try:
                    p['declared'] = obj['innings'][i]['declared']
                except KeyError:
                    p['declared'] = False

                try:
                    p['forfeited'] = obj['innings'][i]['forfeited']
                except KeyError:
                    p['forfeited'] = False

                try:
                    p['target_runs'] = obj['innings'][i]['target']['runs']
                except KeyError:
                    p['target_runs'] = None

                try:
                    p['target_overs'] = obj['innings'][i]['target']['overs']
                except KeyError:
                    p['target_overs'] = None

                try:
                    p['super_over'] = obj['innings'][i]['super_over']
                except KeyError:
                    p['super_over'] = False

                try:
                    if obj['innings'][i]['powerplays']:
                        p['powerplays'] = {
                            'data': []
                        }

                        for j, pp in enumerate(obj['innings'][i]['powerplays']):
                            x = {'start': str(pp['from']), 'end': str(pp['to']), 'type': pp['type']}
                            p['powerplays']['data'].append(x)
                except KeyError:
                    p['powerplays'] = None

                innings.append(p)
            data = {'model': model, 'fields': innings}
            return data


class FixtureOfficials(BaseBuild):
    @classmethod
    def build_data(cls, path, **kwargs):
        model = "fixture.FixtureOfficials"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            fixture_officials_list = list()
            for key in obj['info']['officials'].keys():
                for official in obj['info']['officials'][key]:
                    p = dict({})
                    p['official_id'] = obj['info']['registry']['people'][official]

                    if key == 'match_referees':
                        p['is_match_referee'] = True
                        p['is_reserve_umpire'] = False
                        p['is_tv_umpire'] = False
                        p['is_umpire'] = False

                    if key == 'reserve_umpires':
                        p['is_match_referee'] = False
                        p['is_reserve_umpire'] = True
                        p['is_tv_umpire'] = False
                        p['is_umpire'] = False

                    if key == 'tv_umpires':
                        p['is_match_referee'] = False
                        p['is_reserve_umpire'] = False
                        p['is_tv_umpire'] = True
                        p['is_umpire'] = False

                    if key == 'umpires':
                        p['is_match_referee'] = False
                        p['is_reserve_umpire'] = False
                        p['is_tv_umpire'] = False
                        p['is_umpire'] = True

                    fixture_officials_list.append(p)
            data = {'model': model, 'fields': fixture_officials_list}
            return data


class FixturePlayingXI(BaseBuild):

    @classmethod
    def build_data(cls, path, **kwargs):
        model = "fixture.FixturePlayingXI"

        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            playing_xi_list = list()
            for key in obj['info']['players'].keys():
                team_id = kwargs.get(key)
                for player in obj['info']['players'][key]:
                    p = dict({})
                    p['player_id'] = obj['info']['registry']['people'][player]
                    p['team_id'] = team_id

                    playing_xi_list.append(p)

            data = {'model': model, 'fields': playing_xi_list}
            return data
