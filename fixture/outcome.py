import json
import asyncio

from graphQL import mutations
from core.common import BaseBuild
from .schema import POST_NEW_OUTCOME
from core.logger import Logger

logger = Logger.get_logger(__name__)


class Outcome(BaseBuild):

    @classmethod
    def build_data(cls, path, **kwargs):
        model = "fixture.Outcome"
        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            p = dict({})
            p['fixture_id'] = int(json_file.name.split('/')[-1].split('.')[0])
            try:
                by = obj['info']['outcome']['by']
            except KeyError as e:
                by = None
            if by is not None:
                try:
                    p['by_innings'] = by['innings']
                except KeyError:
                    p['by_innings'] = None

                try:
                    p['by_runs'] = by['runs']
                except KeyError:
                    p['by_runs'] = None

                try:
                    p['by_wickets'] = by['wickets']
                except KeyError:
                    p['by_wickets'] = None

            try:
                p['by_bowl_out_id'] = kwargs.get(obj['info']['outcome']['bowl_out'])
            except KeyError:
                p['by_bowl_out_id'] = None

            try:
                p['by_eliminator_id'] = kwargs.get(obj['info']['outcome']['eliminator'])
            except KeyError:
                p['by_eliminator_id'] = None

            try:
                p['method'] = obj['info']['outcome']['method']
            except KeyError:
                p['method'] = None

            try:
                p['result'] = obj['info']['outcome']['result']
            except KeyError:
                p['result'] = None

            try:
                p['winner_id'] = kwargs.get(obj['info']['outcome']['winner'])
            except KeyError:
                p['winner_id'] = None

            data = {'model': model, 'fields': p}
            return data
