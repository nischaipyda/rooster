import json
import asyncio
from core.common import BaseBuild
from fixture.utils import get_team_by_name
from graphQL import mutations
from .schema import POST_NEW_VERSUS
from core.logger import Logger

logger = Logger.get_logger(__name__)


class FixtureTeams(BaseBuild):

    @classmethod
    def build_data(cls, path, **kwargs):
        model = "fixture.FixtureTeams"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            p = dict({})
            p['fixture_id'] = int(json_file.name.split('/')[-1].split('.')[0])
            p['team_a_id'] = get_team_by_name(obj['info']['teams'][0])[0]['id']
            p['team_b_id'] = get_team_by_name(obj['info']['teams'][1])[0]['id']
            p[obj['info']['teams'][0]] = p['team_a_id']
            p[obj['info']['teams'][1]] = p['team_b_id']

            data = {'model': model, 'fields': p}
            return data
