import json
import asyncio
from graphQL import mutations
from core.common import BaseBuild
from fixture.utils import get_number_with_zero_prefix
from .schema import BULK_POST_NEW_DELIVERY
from core.logger import Logger

logger = Logger.get_logger(__name__)


def get_unique_delivery_number(fixture, innings, over, ball):
    fixture = get_number_with_zero_prefix(fixture, 9)
    innings = get_number_with_zero_prefix(innings, 2)
    over = get_number_with_zero_prefix(over, 3)
    ball = get_number_with_zero_prefix(ball, 2)

    return "10" + fixture + innings + over + ball


class Delivery(BaseBuild):

    @classmethod
    def build_data(cls, path, **kwargs):
        model = 'delivery.Delivery'

        with open(path, 'r') as json_file:
            obj = json.load(json_file)
            delivery_list = list()
            fixture = json_file.name.split('/')[-1].split('.')[0]
            for i, inning in enumerate(obj['innings']):
                for over in inning['overs']:
                    for d, delivery in enumerate(over['deliveries']):
                        p = dict({})
                        innings_key = "{}_{}".format("innings", str(i + 1))
                        temp = over['deliveries'][d]
                        p['innings_id'] = kwargs.get(innings_key)
                        p['over'] = over['over']
                        p['ball'] = d + 1

                        p['unique_delivery_number'] = get_unique_delivery_number(
                            fixture, p['innings_id'], p['over'], p['ball'])

                        registry = obj['info']['registry']['people']
                        p['batter_id'] = registry[delivery['batter']]
                        p['non_striker_id'] = registry[delivery['non_striker']]
                        p['bowler_id'] = registry[delivery['bowler']]

                        p['runs_by_batter'] = delivery['runs']['batter']
                        p['runs_from_extras'] = delivery['runs']['extras']
                        p['runs_total'] = delivery['runs']['total']
                        try:
                            p['is_non_boundary'] = delivery['runs']['non_boundary']
                        except KeyError:
                            p['is_non_boundary'] = False

                        # ****** EXTRAS ******
                        try:
                            p['byes'] = temp['extras']['byes']
                        except KeyError:
                            p['byes'] = 0

                        try:
                            p['leg_byes'] = temp['extras']['legbyes']
                        except KeyError:
                            p['leg_byes'] = 0

                        try:
                            p['no_balls'] = temp['extras']['noballs']
                        except KeyError:
                            p['no_balls'] = 0

                        try:
                            p['penalty'] = temp['extras']['penalty']
                        except KeyError:
                            p['penalty'] = 0

                        try:
                            p['wides'] = temp['extras']['wides']
                        except KeyError:
                            p['wides'] = 0

                        # ****** WICKETS ******
                        try:
                            wickets_list = list()
                            for x, wicket in enumerate(delivery['wickets']):
                                w = dict()
                                try:
                                    w['wicket_kind'] = wicket['kind']
                                except KeyError:
                                    w['wicket_kind'] = None
                                try:
                                    w['player_out_id'] = registry[wicket['player_out']]
                                except KeyError:
                                    w['player_out_id'] = None
                                try:
                                    w['fielder_1_id'] = registry[wicket['fielders'][0]['name']]
                                except KeyError:
                                    w['fielder_1_id'] = None
                                try:
                                    w['is_fielder_1_substitute'] = wicket['fielders'][0]['substitute']
                                except KeyError:
                                    w['is_fielder_1_substitute'] = False
                                try:
                                    w['fielder_2_id'] = registry[wicket['fielders'][1]['name']]
                                except (KeyError, IndexError):
                                    w['fielder_2_id'] = None
                                try:
                                    w['is_fielder_2_substitute'] = wicket['fielders'][1]['substitute']
                                except (KeyError, IndexError):
                                    w['is_fielder_2_substitute'] = False

                                wickets_list.append(w)
                            p['wickets'] = {'data': wickets_list}
                            del wickets_list
                        except KeyError:
                            del wickets_list
                            pass

                        # ****** Review ******
                        try:
                            r = dict()
                            r['delivery_id'] = p['unique_delivery_number']
                            r['batter_id'] = registry[delivery['review']['batter']]
                            r['by_team_id'] = kwargs.get(delivery['review']['by'])
                            r['decision'] = delivery['review']['decision']
                            try:
                                r['umpire_id'] = registry[delivery['review']['umpire']]
                            except KeyError:
                                r['umpire_id'] = None
                            try:
                                r['umpires_call'] = delivery['review']['umpires_call']
                            except KeyError:
                                r['umpires_call'] = False
                            p['review'] = {'data': r}
                        except KeyError:
                            del r
                            pass

                        # ****** Replacement ******
                        try:
                            replacement_list = []
                            for replacement_type in delivery['replacements'].keys():
                                for replacement in delivery['replacements'][replacement_type]:
                                    q = dict()
                                    q['type'] = replacement_type
                                    q['player_in_id'] = registry[replacement['in']]
                                    q['player_out_id'] = registry[replacement['out']]
                                    q['reason'] = replacement['reason']
                                    try:
                                        q['team_id'] = kwargs.get(replacement['team'])
                                    except KeyError:
                                        q['team_id'] = None

                                    try:
                                        q['role'] = replacement['role']
                                    except KeyError:
                                        q['role'] = None
                                    replacement_list.append(q)
                            p['replacements'] = {'data': replacement_list}
                        except KeyError:
                            del replacement_list
                            pass

                        delivery_list.append(p)

            data = {'model': model, 'fields': delivery_list}
            with open('delivery.json', 'w') as fs:
                fs.write(json.dumps(data))
            return data

    @classmethod
    def mutate(cls, data, **kwargs):
        result = asyncio.run(mutations.bulk_mutation(mutation_type=BULK_POST_NEW_DELIVERY, data=data['fields']))

        return {'delivery_id': None}
