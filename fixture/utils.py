import asyncio
from graphQL import query
from team.schema import GET_TEAM_BY_NAME
from core.exceptions import NonSingularResponseError


def get_team_by_name(name):
    result = asyncio.run(query.core_query({"name": name}, GET_TEAM_BY_NAME))
    teams = result['team']
    if not teams:
        return None
    if len(teams) == 1:
        return teams
    if len(teams) > 1:
        raise NonSingularResponseError("Number of teams with the given filter is more than 1.")


def get_number_with_zero_prefix(number, divisor):
    length = len(str(number))
    return '0' * (divisor - (length % divisor)) + str(number)


def convert_to_base64(words):
    import base64
    words_bytes = words.encode("ascii")
    return base64.b64encode(words_bytes).decode('ascii')
