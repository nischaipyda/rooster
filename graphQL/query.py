import traceback
from aiohttp.client_exceptions import ClientConnectorError
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError
from core.exceptions import TerminateRuntime

from core.logger import Logger

logger = Logger.get_logger(__name__)
transport = AIOHTTPTransport(url="http://localhost:8080/v1/graphql")


async def core_query(data, query_type):
    try:
        query = gql(query_type)
        async with Client(transport=transport, serialize_variables=False) as session:
            result = await session.execute(query, variable_values=data)
            return result
    except TransportQueryError as e:
        traceback.print_exc()
        logger.error("<TransportQueryError>:Error<{}>".format(repr(e)))
    except (ClientConnectorError, TransportServerError) as e:
        raise TerminateRuntime("<ClientConnectorError>:Error<{}>".format(repr(e)))
    except Exception as e:
        traceback.print_exc()
        logger.error("<{}>:Error<{}>".format(type(e), repr(e)))


async def query_by_id(data, query_type):
    try:
        query = gql(query_type)
        async with Client(transport=transport, serialize_variables=False) as session:
            result = await session.execute(query, variable_values=data)
            return result
    except TransportQueryError as e:
        traceback.print_exc()
        logger.error("<TransportQueryError>:Error<{}>".format(repr(e)))
    except (ClientConnectorError, TransportServerError) as e:
        raise TerminateRuntime("<ClientConnectorError>:Error<{}>".format(repr(e)))
    except Exception as e:
        traceback.print_exc()
        logger.error("<{}>:Error<{}>".format(type(e), repr(e)))
