import asyncio
from graphQL import query
from .schema import GET_CITY_BY_NAME
from core.exceptions import NonSingularResponseError


def get_city_by_name(name):
    result = asyncio.run(query.core_query({"name": name}, GET_CITY_BY_NAME))
    city = result['cities']['edges']
    if not city:
        return None
    if len(city) == 1:
        return city
    if len(city) > 1:
        raise NonSingularResponseError("Number of teams with the given filter is more than 1.")
