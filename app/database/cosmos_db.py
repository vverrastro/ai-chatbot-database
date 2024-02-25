from azure.cosmos import CosmosClient, exceptions
from .base_db import DatabaseConnection

class CosmosDBConnection(DatabaseConnection):
    def __init__(self, uri, primary_key, database_name, container_name):
        super().__init__(uri=uri, primary_key=primary_key, database_name=database_name, container_name=container_name)
        self.client = None
        self.database = None
        self.container = None
        self.connect()

    def connect(self):
        """
        Establishes a connection to the CosmosDB database and container.
        """
        try:
            # Initialize the Cosmos client
            self.client = CosmosClient(self.connection_details["uri"], credential=self.connection_details["primary_key"])
            # Get a reference to the database
            self.database = self.client.get_database_client(self.connection_details["database_name"])
            # Get a reference to the container
            self.container = self.database.get_container_client(self.connection_details["container_name"])
            
            print("Connection to Azure CosmosDB established successfully.")
        except exceptions.CosmosHttpResponseError as e:
            print(f"Failed to connect to CosmosDB: {e}")

    def test_connection(self):
        """
        Tests the connection to the CosmosDB by trying to list the containers in the database
        and performing a simple query on a specified container.
        Returns True if successful, False otherwise.
        """
        try:
            # Attempt to list containers to test the connection
            containers = list(self.database.list_containers())
            print("Containers in the database:", [container['id'] for container in containers])

            # Perform a simple query (adjust 'your_container_name' and the query as needed)
            container_name = "transcript-conversations"
            container = self.database.get_container_client(container_name)
            query = "SELECT * FROM c OFFSET 0 LIMIT 5"  # Adjust the query as needed
            items = list(container.query_items(query=query, enable_cross_partition_query=True))
            
            # Print the items retrieved by the query
            print(f"Items from {container_name}:")
            for item in items:
                print(item)
        
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def execute_query(self, query):
        """
        Executes a query against the CosmosDB container.
        """
        try:
            items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
            return items
        except exceptions.CosmosHttpResponseError as e:
            print(f"Query failed: {e}")
            return []

    def close_connection(self):
        """
        Closes the connection to CosmosDB. Since the CosmosClient doesn't have a close method,
        this method can be used to manually clean up resources, if necessary.
        """
        self.client = None
        self.database = None
        self.container = None
        print("Connection to Azure CosmosDB closed.")