import traceback
from aiohttp.client_exceptions import ClientConnectorError

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError

from core.logger import Logger
from core.exceptions import RoosterGraphQLError, TerminateRuntime

logger = Logger.get_logger(__name__)
transport = AIOHTTPTransport(url="http://localhost:8080/v1/graphql")


async def core_mutation(data, mutation_type):
    try:
        doc = gql(mutation_type)
        async with Client(transport=transport, serialize_variables=True) as session:
            result = await session.execute(doc, variable_values={"input": data})
            return result
    except TransportQueryError as e:
        traceback.print_exc()
        logger.error("<TransportQueryError>:Error<{}>".format(repr(e)))
        raise Exception(repr(e))
    except (ClientConnectorError, TransportServerError) as e:
        raise TerminateRuntime("<ClientConnectorError>:{}".format(repr(e)))
    except Exception as e:
        traceback.print_exc()
        logger.error("<{}>:Error<{}>".format(type(e), repr(e)))
        raise Exception(type(e), repr(e))


async def bulk_mutation(data, mutation_type):
    if type(data) is not list:
        raise TypeError(
            "'{}' expects {} type but got {} at argument 1.".format(bulk_mutation.__name__, type([]), type(data)))

    try:
        query = gql(mutation_type)
        async with Client(transport=transport, serialize_variables=False, execute_timeout=600) as session:
            result = await session.execute(query, variable_values={"input": data})
            return result
    except TransportQueryError as e:
        errors = ['Uniqueness violation. duplicate key value violates unique constraint "wicket_delivery_id_player_out_id_7bd05189_uniq"']
        if e.errors[0]['message'] in errors:
            pass
        else:
            print(traceback.print_exc())
            logger.error("<TransportQueryError>:Error<{}>".format(repr(e)))
            raise Exception(repr(e))
    except (ClientConnectorError, TransportServerError) as e:
        print(traceback.print_exc())
        raise TerminateRuntime("<ClientConnectorError>:Error<{}>".format(repr(e)))
    except Exception as e:
        print(traceback.print_exc())
        logger.error("<{}>:Error<{}>".format(type(e), repr(e)))
        raise Exception(repr(e))


async def update_mutation(data, mutation_type):
    try:
        doc = gql(mutation_type)
        async with Client(transport=transport, serialize_variables=True) as session:
            result = await session.execute(doc, variable_values=data)
            return result
    except TransportQueryError as e:
        traceback.print_exc()
        logger.error("<TransportQueryError>:Error<{}>".format(repr(e)))
        raise Exception(repr(e))
    except (ClientConnectorError, TransportServerError) as e:
        raise TerminateRuntime("<ClientConnectorError>:{}".format(repr(e)))
    except Exception as e:
        traceback.print_exc()
        logger.error("<{}>:Error<{}>".format(type(e), repr(e)))
        raise Exception(repr(e))
