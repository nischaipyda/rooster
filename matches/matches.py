import json
from core.common import MatchFilePath
from series.series import Series
from tournament.tournament import Tournament, Group
from delivery.delivery import Delivery
from fixture.fixture import (
    Toss,
    Outcome,
    Innings,
    FixtureOfficials,
    Fixture,
    FixturePlayingXI
)


class BaseMatch:

    @classmethod
    def build_series(cls):
        data = Series.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_tournament(cls, series_id):
        data = Tournament.build_data(MatchFilePath.input, series_id=series_id)
        return data

    @classmethod
    def build_group(cls, tournament_id):
        data = Group.build_data(MatchFilePath.input, tournament_id=tournament_id)
        return data

    @classmethod
    def build_toss(cls):
        data = Toss.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_outcome(cls):
        data = Outcome.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_versus(cls):
        # TODO: versus.build_data
        data = Outcome.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_fixture(cls, **kwargs):
        data = Fixture.build_data(MatchFilePath.input, **kwargs)
        return data

    @classmethod
    def build_innings(cls):
        data = Innings.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_fixture_officials(cls):
        data = FixtureOfficials.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_playingxi_fixture(cls):
        data = FixturePlayingXI.build_data(MatchFilePath.input)
        return data

    @classmethod
    def build_delivery(cls):
        data = Delivery.build_data(MatchFilePath.input)
        return data

    @classmethod
    def run(cls):
        # TODO: mutation should be performed as intermediate step for it to return global ids
        # series = cls.build_series()
        # tournament = cls.build_tournament(series['id'])
        # group = cls.build_group(tournament_id='9999')
        # toss = cls.build_toss()
        # outcome = cls.build_outcome()
        # fixture = cls.build_fixture(tournament_id='9999', outcome_id='999', versus_id='999', toss_id='999')
        # playingXI = cls.build_playingxi_fixture()
        # fixture_officials = cls.build_fixture_officials()
        # innings = cls.build_innings()
        # delivery = cls.build_delivery()
        with open('silly.json', 'w') as outf:
            outf.write(json.dumps(series))
