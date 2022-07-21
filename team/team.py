import json

from settings import BAKE_DIR, MATCHES_DIR
from core.parser import BaseParser
from core.utils import get_x_dataframe_from_csv, build_short_name, build_overview_csv_file
from core.mixins import MutateMixins
from graphQL import mutations
from core.logger import Logger
from .schema import POST_NEW_TEAM

logger = Logger.get_logger(__name__)


def get_fixture_overview_dataframe(path=BAKE_DIR / 'overview.csv'):
    df = get_x_dataframe_from_csv(path)
    return df


class Team(BaseParser):
    class Meta:
        input_file_path = MATCHES_DIR / 'README.txt'
        output_file_name = "teams.json"

    @classmethod
    def clean_input(cls, camel_case=True, **kwargs):
        build_overview_csv_file(cls._meta.input_file_path)

    @classmethod
    def build_data(cls, **kwargs):
        df = get_fixture_overview_dataframe()
        teams = []
        unique_teams_set = set()

        for i, row in df.iterrows():
            a = dict()
            b = dict()
            u_teamA = row['teamA'] + "_" + row["pool"] + "_" + row["gender"]
            u_teamB = row['teamB'] + "_" + row["pool"] + "_" + row["gender"]

            # team A
            if u_teamA not in unique_teams_set:
                a["name"] = str(row["teamA"]).strip()
                a["short_name"] = build_short_name(a["name"])
                a["pool"] = row["pool"]
                a["gender"] = row["gender"]
                a["primary_color"] = None
                a["secondary_color"] = None
                a["city_id"] = None
                a["country_id"] = None
                teams.append(a)
            # team B
            if u_teamB not in unique_teams_set:
                b["name"] = str(row["teamB"]).strip()
                b["short_name"] = build_short_name(b["name"])
                b["pool"] = row["pool"]
                b["gender"] = row["gender"]
                b["primary_color"] = None
                b["secondary_color"] = None
                b["city_id"] = None
                b["country_id"] = None
                teams.append(b)

            unique_teams_set.update([u_teamA, u_teamB])

        temp = cls._get_temp_file_path()
        with open(temp, 'w') as out:
            out.write(json.dumps(teams))

        data = super().build_data(**kwargs)
        return data

    @classmethod
    def mutate(cls):
        MutateMixins.bulk_mutate(mutations.bulk_mutation, mutation_type=POST_NEW_TEAM, file=cls._get_bake_file_path())
