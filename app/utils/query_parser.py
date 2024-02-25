
def parse_natural_language_to_query(nl_input, db_type):
    """
    Dummy function to convert natural language input to a database query.
    This is a placeholder and should be replaced with actual NLP logic or integration with an NLP service.
    
    :param nl_input: User input in natural language
    :param db_type: Type of database (e.g., 'Azure CosmosDB', 'MySQL', 'PostgreSQL')
    :return: A string representing a basic query based on the input
    """
    # Placeholder logic for demonstration purposes
    if db_type == "Azure CosmosDB":
        return f"SELECT * FROM c WHERE CONTAINS(c.description, '{nl_input}', true)"
    elif db_type == "MySQL" or db_type == "PostgreSQL":
        return f"SELECT * FROM table WHERE description LIKE '%{nl_input}%'"
    else:
        return "Unsupported database type"