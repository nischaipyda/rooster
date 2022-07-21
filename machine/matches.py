import sys
import json
import logging
import traceback
import os

from transitions import Machine
from core.common import MatchFilePath
from settings import MATCHES_BUILD

logging.basicConfig(level=logging.DEBUG, filename="./logs/machine.log")
logging.getLogger('transitions').setLevel(logging.INFO)


class MatchesStateMachine(Machine):

    def __init__(self):
        self.temp = []
        self.filter_data = dict()
        self.global_ids = dict()
        self.global_ids['fixture'] = {}
        states = [
            {'name': 'INIT'},
            {'name': 'VERSUS_BUILD', 'on_enter': self.cache_data},
            # {'name': 'VERSUS_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'SERIES_BUILD', 'on_enter': self.cache_data},
            {'name': 'SERIES_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'TOURNAMENT_BUILD', 'on_enter': self.cache_data},
            {'name': 'TOURNAMENT_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'GROUP_BUILD', 'on_enter': self.cache_data},
            {'name': 'GROUP_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'TOSS_BUILD', 'on_enter': self.cache_data},
            {'name': 'TOSS_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'OUTCOME_BUILD', 'on_enter': self.cache_data},
            {'name': 'OUTCOME_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'VENUE_BUILD', 'on_enter': self.cache_data},
            {'name': 'VENUE_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'FIXTURE_BUILD', 'on_enter': self.cache_data},
            {'name': 'FIXTURE_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'INNINGS_BUILD', 'on_enter': self.cache_data},
            {'name': 'INNINGS_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'FIXTURE_OFFICIALS_BUILD', 'on_enter': self.cache_data},
            {'name': 'FIXTURE_OFFICIALS_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'PLAYING_XI_BUILD', 'on_enter': self.cache_data},
            {'name': 'PLAYING_XI_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'DELIVERY_BUILD', 'on_enter': self.cache_data},
            {'name': 'DELIVERY_MUTATE', 'on_enter': self.mutate_data},
            {'name': 'TERMINATE', 'on_enter': self.write_to_file}
        ]

        transitions = [
            {'trigger': 'init', 'source': '*', 'dest': 'INIT'},

            {'trigger': 'versus_create', 'source': 'INIT', 'dest': 'VERSUS_BUILD'},

            {'trigger': 'series_create', 'source': 'VERSUS_BUILD', 'dest': 'SERIES_BUILD'},
            {'trigger': 'series_save', 'source': 'SERIES_BUILD', 'dest': 'SERIES_MUTATE', 'unless': 'is_exists'},

            {'trigger': 'tournament_create', 'source': ['SERIES_MUTATE', 'SERIES_BUILD'], 'dest': 'TOURNAMENT_BUILD'},
            {'trigger': 'tournament_save', 'source': 'TOURNAMENT_BUILD', 'dest': 'TOURNAMENT_MUTATE',
             'unless': 'is_exists'},

            {'trigger': 'group_create', 'source': ['TOURNAMENT_BUILD', 'TOURNAMENT_MUTATE'], 'dest': 'GROUP_BUILD'},
            {'trigger': 'group_save', 'source': 'GROUP_BUILD', 'dest': 'GROUP_MUTATE', 'unless': 'is_exists'},

            {'trigger': 'toss_create', 'source': ['GROUP_BUILD', 'GROUP_MUTATE'], 'dest': 'TOSS_BUILD'},

            {'trigger': 'outcome_create', 'source': 'TOSS_BUILD', 'dest': 'OUTCOME_BUILD'},

            {'trigger': 'venue_create', 'source': 'OUTCOME_BUILD', 'dest': 'VENUE_BUILD'},

            {'trigger': 'innings_create', 'source': 'VENUE_BUILD', 'dest': 'INNINGS_BUILD'},

            {'trigger': 'fixture_officials_create', 'source': 'INNINGS_BUILD', 'dest': 'FIXTURE_OFFICIALS_BUILD'},

            {'trigger': 'playing_xi_create', 'source': 'FIXTURE_OFFICIALS_BUILD', 'dest': 'PLAYING_XI_BUILD'},

            {'trigger': 'fixture_create', 'source': 'PLAYING_XI_BUILD', 'dest': 'FIXTURE_BUILD'},
            {'trigger': 'fixture_save', 'source': 'FIXTURE_BUILD', 'dest': 'FIXTURE_MUTATE', 'unless': 'is_exists'},

            {'trigger': 'delivery_create', 'source': ['FIXTURE_MUTATE', 'FIXTURE_BUILD'], 'dest': 'DELIVERY_BUILD'},
            {'trigger': 'delivery_save', 'source': 'DELIVERY_BUILD', 'dest': 'DELIVERY_MUTATE'},

            {'trigger': 'stop', 'source': ['DELIVERY_BUILD', 'DELIVERY_MUTATE'], 'dest': 'TERMINATE'},
            {
                'trigger': 'internal_state_update',
                'source': ['SERIES_BUILD', 'TOURNAMENT_BUILD', 'GROUP_BUILD'],
                'dest': None,
                'after': 'update_data'
            },

        ]
        Machine.__init__(self, states=states, transitions=transitions, send_event=True, auto_transitions=False,
                         initial='INIT', on_exception=self.handle_error)

    def cache_data(self, event):
        print("Prepare", event.state.value)
        fixture_states = ['TOSS_BUILD', 'OUTCOME_BUILD', 'VENUE_BUILD', 'INNINGS_BUILD', 'FIXTURE_OFFICIALS_BUILD',
                          'PLAYING_XI_BUILD']
        Model = event.kwargs.get('cls_type')
        current_state = event.state.value

        self.filter_data = Model.build_data(MatchFilePath.input, **self.global_ids)
        if current_state == 'VERSUS_BUILD':
            self.global_ids.update(self.filter_data['fields'])
        if current_state in fixture_states:
            temp = str(current_state).lower().split("_")
            key = "_".join(temp[:-1])
            self.global_ids['fixture'][key] = self.filter_data['fields']
        if self.filter_data:
            if type(self.filter_data) is list:
                self.temp.extend(self.filter_data)
            else:
                self.temp.append(self.filter_data)

    def mutate_data(self, event):
        if self.filter_data:
            Model = event.kwargs.get('cls_type')
            result = Model.mutate(data=self.filter_data)
            if result and type(result) is dict:
                self.global_ids.update(result)
            else:
                raise Exception("Error occurred while trying to insert {}.\n Following was returned:\n{}",
                                self.filter_data, result)

    def is_exists(self, event):
        if self.filter_data:
            Model = event.kwargs.get('cls_type')
            current_state = event.transition.dest
            data = Model.exists(**self.filter_data['fields'])

            if data is None:
                return False
            elif type(data) is list:
                self.global_ids[str(current_state).lower().split("_")[0]] = data[0]['id']
                return True
            elif type(data) is dict:
                self.global_ids.update(data)
                pass

    def update_data(self, event):
        print("updating data in ", event.transition.source, event.transition.dest)
        if self.filter_data:
            Model = event.kwargs.get('cls_type')
            result = Model.update(self.filter_data, **self.global_ids)

    def write_to_file(self, event):
        with open(MATCHES_BUILD / os.path.basename(MatchFilePath.input), 'w+') as out:
            out.write(json.dumps(self.temp))

    def handle_error(self, event):
        traceback.print_exc()
        print(event.state.value, event.error)
        sys.exit(event.error)
