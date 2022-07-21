class ImproperlyConfigured(Exception):
    """Parser is somehow improperly configured"""
    pass


class RoosterGraphQLError(Exception):
    """Errors array in the GraphQL response is not null"""
    pass


class TerminateRuntime(Exception):
    """Terminate the program"""
    pass


class NonSingularResponseError(Exception):
    """Response contains more than 1 nodes"""
    pass
