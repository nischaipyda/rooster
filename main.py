from machine.matches import MatchesStateMachine
from core.common import MatchFilePath, get_file_name
from series.series import Series
from tournament.tournament import Tournament, Group
from fixture.fixture import Fixture, Innings, FixtureOfficials, FixturePlayingXI
from fixture.outcome import Outcome
from fixture.toss import Toss
from fixture.versus import FixtureTeams
from delivery.delivery import Delivery
from location.location import Venue
from settings import MATCHES_DIR

print('hello')
# files = get_file_name()
files = ['1254102.json']
for i, file in enumerate(files):
    MatchFilePath.input = MATCHES_DIR / file
    first = MatchesStateMachine()
    first.versus_create(cls_type=FixtureTeams)
    first.series_create(cls_type=Series)
    first.series_save(cls_type=Series)
    if first.state == 'SERIES_BUILD':
        first.internal_state_update(cls_type=Series)

    first.tournament_create(cls_type=Tournament)
    first.tournament_save(cls_type=Tournament)
    if first.state == 'TOURNAMENT_BUILD':
        first.internal_state_update(cls_type=Tournament)
    first.group_create(cls_type=Group)
    first.group_save(cls_type=Group)
    if first.state == 'GROUP_BUILD':
        first.internal_state_update(cls_type=Group)
    first.toss_create(cls_type=Toss)
    first.outcome_create(cls_type=Outcome)
    first.venue_create(cls_type=Venue)
    first.innings_create(cls_type=Innings)
    first.fixture_officials_create(cls_type=FixtureOfficials)
    first.playing_xi_create(cls_type=FixturePlayingXI)
    first.fixture_create(cls_type=Fixture)
    first.fixture_save(cls_type=Fixture)
    first.delivery_create(cls_type=Delivery)
    first.delivery_save(cls_type=Delivery)
    first.stop()
    del first
