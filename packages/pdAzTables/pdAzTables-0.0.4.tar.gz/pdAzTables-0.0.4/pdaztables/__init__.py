from azure.cosmosdb.table.tableservice import TableService
import pandas

class AzTable():
    """
    Main class to manage and simplify connection from Azure Table Storage to/from a Pandas DataFrame.
    """

    def __init__(self, connection_string=None, account_name=None, account_key=None, sas_token=None):
        """Create service object with different authentication options.

        You can use:
            1) Just connection_string
            2) Provide account_name and account_key
            3) Provide account_name and a sas_token

        Args:
            connection_string : String
                Full connection string to the Azure Data Lake
            account_name : String
                The storage account name. This is used to authenticate requests 
            signed with an account key and to construct the storage endpoint. It 
            is required unless a connection string is given.
            account_key : String
                The storage account key. This is used for shared key authentication. 
            sas_token : String
                A shared access signature token to use to authenticate requests 
             instead of the account key.
        """
        
        if connection_string:
            self.table_service = TableService(connection_string=connection_string)
        elif account_name:
            if account_key:
                self.table_service = TableService(account_name=account_name, account_key=account_key)
            elif sas_token:
                self.table_service = TableService(account_name=account_name, sas_token=sas_token)

    def get_table(self, table_name, n_rows=None):
        """Gets a table from ADLS and returns a Pandas DataFrame

        Args:
            table_name : String
                Name of the table in the data lake's table storage.
            n_rows : int
                Number of rows to get from the table (will get first N rows).

        Returns:
            Pandas.DataFrame: DataFrame containing the table data.
        """

        return pandas.DataFrame(self.__get_data_from_table_storage_table(self.table_service, table_name, n_rows))

    def list_tables(self):
        """Get a list of table names in the table service.

        Returns:
            List: list of table names
        """

        iter = self.table_service.list_tables()
        ret = list()
        for i in iter.items:
            ret.append(i.name)

        return ret

    def __get_data_from_table_storage_table(self, table_service, table_name, n_rows):
        """ Retrieve data from Table Storage """

        SOURCE_TABLE = table_name
        for record in table_service.query_entities(SOURCE_TABLE, num_results=n_rows
        ):
            yield record