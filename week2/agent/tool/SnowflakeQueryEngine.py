"""
Snowflake Database Tool for AutoGen Agents

This module provides a SnowflakeQueryTool class that can be wrapped in AutoGen's FunctionTool
to enable agents to connect to and query Snowflake databases.

This tool uses Personal Access Token (PAT) authentication only for secure, programmatic access.

Environment Variables Required:
- SNOWFLAKE_ACCOUNT: Snowflake account identifier (required)
- SNOWFLAKE_USER: Username for authentication (required)
- SNOWFLAKE_TOKEN: Personal Access Token (PAT) for OAuth authentication (required)

Optional Parameters:
- SNOWFLAKE_WAREHOUSE: Warehouse name (optional, can be set in connection)
- SNOWFLAKE_DATABASE: Database name (optional, can be set in connection)  
- SNOWFLAKE_SCHEMA: Schema name (optional, can be set in connection)
- SNOWFLAKE_ROLE: Role name (optional)

Note: This tool only supports PAT token authentication for security and automation purposes.
To obtain a PAT token, log into Snowflake and generate one from your user profile settings.

"""

import os
import logging
from typing import Dict, Any, Optional, List
from contextlib import contextmanager
import pandas as pd
import snowflake.connector
from snowflake.connector import DictCursor
from dotenv import load_dotenv


class SnowflakeQueryEngine:
    """
    A tool class for executing queries against Snowflake database.
    
    This class handles connection management, query execution, and error handling
    for Snowflake database operations. It's designed to be used with AutoGen's
    FunctionTool wrapper.
    
    Attributes:
        connection_params (Dict[str, Any]): Snowflake connection parameters
        _connection (Optional): Current database connection
    """
    
    def __init__(self):
        """
        Initialize the SnowflakeQueryTool with connection parameters from environment variables.
        
        Raises:
            ValueError: If required environment variables are missing
            ImportError: If snowflake-connector-python is not installed
        """
        # TODO: Student Implementation
        # 1. Load environment variables from a .env file if present
        #    Hint: Use load_dotenv()
        
        # 2. Load connection parameters from environment variables
        #    Hint: Use self._load_connection_params() and store in self.connection_params
        
        # 3. Initialize the connection variable
        #    Hint: Set self._connection to None initially
        
        # 4. Set up logging configuration
        #    - Get log level from environment variable 'LOG_LEVEL' (default to 'ERROR')
        #    - Convert to uppercase
        #    - Set up basic logging configuration
        #    - Create a logger instance for this class
        
        raise NotImplementedError("Student must implement the __init__ method")
        
    def _load_connection_params(self) -> Dict[str, Any]:
        """
        Load Snowflake connection parameters from environment variables.
        
        Returns:
            Dict[str, Any]: Connection parameters dictionary
            
        Raises:
            ValueError: If required environment variables are missing
        """
        # TODO: Student Implementation
        # 1. Define required parameters dictionary with keys: 'account', 'user', 'password'
        #    Map to environment variables: 'SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD'
        
        # 2. Define optional parameters dictionary with keys: 'warehouse', 'database', 'schema', 'role'
        #    Map to corresponding SNOWFLAKE_* environment variables
        
        # 3. Create empty params dictionary
        
        # 4. Check and add required parameters
        #    - Use os.getenv() to get values
        #    - Raise ValueError if any required parameter is missing
        
        # 5. Add optional parameters if available
        
        # 6. Add additional connection settings:
        #    - client_session_keep_alive: True
        #    - autocommit: True
        #    - application: 'AutoGen_SnowflakeQueryTool'
        
        # 7. Return the params dictionary
        
        raise NotImplementedError("Student must implement the _load_connection_params method")
    
    def _create_connection(self):
        """
        Create a new Snowflake connection using the configured parameters.
        
        Returns:
            snowflake.connector.connection: Snowflake database connection
            
        Raises:
            Exception: If connection fails
        """
        # TODO: Student Implementation
        # 1. Log info message about creating connection
        #    Hint: Use self.logger.info()
        
        # 2. Create connection using snowflake.connector.connect()
        #    Hint: Pass self.connection_params using **kwargs syntax
        
        # 3. Log success message
        
        # 4. Return the connection object
        
        # 5. Handle exceptions:
        #    - Log error message with exception details
        #    - Re-raise the exception
        
        raise NotImplementedError("Student must implement the _create_connection method")
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections with automatic cleanup.
        
        Yields:
            snowflake.connector.connection: Database connection
        """
        # TODO: Student Implementation
        # 1. Initialize connection variable to None
        
        # 2. In try block:
        #    - Create connection using self._create_connection()
        #    - Yield the connection
        
        # 3. In except block:
        #    - Log error message
        #    - Re-raise exception
        
        # 4. In finally block:
        #    - If connection exists, try to close it
        #    - Log appropriate messages
        #    - Handle any closing exceptions
        
        raise NotImplementedError("Student must implement the _get_connection method")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Snowflake connection and return connection details.
        
        Returns:
            Dict[str, Any]: Connection test results
        """
        # TODO: Student Implementation
        # 1. Use self._get_connection() context manager
        
        # 2. Create cursor and execute:
        #    "SELECT CURRENT_VERSION() as version, CURRENT_WAREHOUSE() as warehouse, 
        #     CURRENT_DATABASE() as database, CURRENT_SCHEMA() as schema, CURRENT_ROLE() as role"
        
        # 3. Fetch the result
        
        # 4. Return success dictionary with:
        #    - success: True
        #    - message: "Connection successful"
        #    - details: dictionary with version, warehouse, database, schema, role
        
        # 5. Handle exceptions and return failure dictionary with:
        #    - success: False
        #    - message: error details
        #    - details: None
        
        raise NotImplementedError("Student must implement the test_connection method")
    
    def execute_query(
        self, 
        query: str, 
        goal: str,
        return_format: str
    ) -> Dict[str, Any]:
        """
        Execute a SQL query against the Snowflake database.
        
        Args:
            query (str): SQL query to execute
            goal (str, optional): Description of what the query is trying to achieve
            return_format (str, optional): Format for returned data ('dict', 'dataframe', 'list')
            
        Returns:
            Dict[str, Any]: Query execution results with metadata
        """
        # TODO: Student Implementation
        # 1. Log the query and goal (if provided)
        
        # 2. Use self._get_connection() context manager
        
        # 3. Create cursor with DictCursor
        
        # 4. Execute the query
        
        # 5. Fetch all results
        
        # 6. Convert results to pandas DataFrame
        
        # 7. Format data based on return_format:
        #    - "dataframe": return the DataFrame
        #    - "list": return the raw results
        #    - default: convert to list of dictionaries
        
        # 8. Return success dictionary with:
        #    - success, data, query, goal, row_count, columns, data_frame, return_format
        
        # 9. Handle exceptions and return error dictionary
        
        raise NotImplementedError("Student must implement the execute_query method")
    
    def get_table_info(self, table_name: str, schema: str, database: str) -> Dict[str, Any]:
        """
        Get information about a specific table including column details.
        
        Args:
            table_name (str): Name of the table
            schema (str, optional): Schema name (uses current schema if not specified)
            database (str, optional): Database name (uses current database if not specified)
            
        Returns:
            Dict[str, Any]: Table information including columns and data types
        """
        # TODO: Student Implementation
        # 1. Build table reference string based on provided parameters
        
        # 2. Construct SQL query to get column information from INFORMATION_SCHEMA.COLUMNS:
        #    - Select: COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, ORDINAL_POSITION, COMMENT
        #    - Filter by TABLE_NAME (and optionally TABLE_SCHEMA and TABLE_CATALOG)
        #    - Order by ORDINAL_POSITION
        
        # 3. Execute query using self.execute_query()
        
        # 4. If successful, return dictionary with:
        #    - success, table_name, schema, database, columns, column_count
        
        # 5. Handle errors appropriately
        
        raise NotImplementedError("Student must implement the get_table_info method")

    def list_tables(self, schema: str, database: str) -> Dict[str, Any]:
        """
        List all tables in the specified schema/database.
        
        Args:
            schema (str, optional): Schema name (uses current schema if not specified)
            database (str, optional): Database name (uses current database if not specified)
            
        Returns:
            Dict[str, Any]: List of tables with metadata
        """
        # TODO: Student Implementation
        # 1. Construct base SQL query to select from INFORMATION_SCHEMA.TABLES:
        #    - Select: TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE, ROW_COUNT, BYTES, COMMENT
        #    - Filter by TABLE_TYPE = 'BASE TABLE'
        
        # 2. Add optional WHERE conditions for schema and database if provided
        
        # 3. Add ORDER BY clause
        
        # 4. Execute query using self.execute_query()
        
        # 5. If successful, return dictionary with:
        #    - success, tables, table_count, schema, database
        
        # 6. Handle errors appropriately
        
        raise NotImplementedError("Student must implement the list_tables method")
