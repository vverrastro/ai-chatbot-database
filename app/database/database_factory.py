from .cosmos_db import CosmosDBConnection

def create_connection(db_type, db_connection, **kwargs):
    """
    Creates a database connection based on the specified database type. 
    Supports 'Default (Azure CosmosDB)' and 'Azure CosmosDB' as database types. 
    Returns a connection object for the specified database.

    :param db_type: A string specifying the type of database to connect to.
    :param db_connection: A dictionary containing the connection details for 'Default (Azure CosmosDB)'.
    :param kwargs: Additional keyword arguments containing the connection details for 'Azure CosmosDB'.
    :return: A connection object for the specified database.
    :raises ValueError: If the specified database type is unsupported.
    """
    if db_type == "Default (Azure CosmosDB)":
        # Create and return a connection object for the default Azure CosmosDB configuration
        return CosmosDBConnection(**db_connection)
    elif db_type == "Azure CosmosDB":
        # Create and return a connection object for Azure CosmosDB using additional keyword arguments
        return CosmosDBConnection(**kwargs)
    else:
        # Raise an error if the database type is not supported
        raise ValueError(f"Unsupported database type: {db_type}")
