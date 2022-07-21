import json
import asyncio
from core.common import BaseBuild
from graphQL import mutations
from .schema import POST_NEW_TOSS
from core.logger import Logger

logger = Logger.get_logger(__name__)


class Toss(BaseBuild):

    @classmethod
    def build_data(cls, path, **kwargs):
        model = "fixture.Toss"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            p = dict({})
            p['fixture_id'] = int(json_file.name.split('/')[-1].split('.')[0])
            p['decision'] = obj['info']['toss']['decision']
            p['winner_id'] = kwargs.get(obj['info']['toss']['winner'])
            try:
                p['uncontested'] = obj['info']['toss']['uncontested']
            except KeyError:
                p['uncontested'] = False
            data = {'model': model, 'fields': p}
            return data
