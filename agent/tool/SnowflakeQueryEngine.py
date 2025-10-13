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
        # Load environment variables from a .env file if present
        load_dotenv()
        # Load connection parameters from environment variables
        self.connection_params = self._load_connection_params()
        self._connection = None
        
        # Set up logging
        logging.basicConfig(level=logging.ERROR)
        self.logger = logging.getLogger(__name__)
    
    def _load_connection_params(self) -> Dict[str, Any]:
        """
        Load Snowflake connection parameters from environment variables.
        
        Returns:
            Dict[str, Any]: Connection parameters dictionary
            
        Raises:
            ValueError: If required environment variables are missing
        """
        required_params = {
            'account': 'SNOWFLAKE_ACCOUNT',
            'user': 'SNOWFLAKE_USER',
            'password': 'SNOWFLAKE_PASSWORD'  # PAT token is now required
        }

        optional_params = {
            'warehouse': 'SNOWFLAKE_WAREHOUSE',
            'database': 'SNOWFLAKE_DATABASE',
            'schema': 'SNOWFLAKE_SCHEMA',
            'role': 'SNOWFLAKE_ROLE'
        }
        
        params = {}
        
        # Check required parameters
        for param_name, env_var in required_params.items():
            value = os.getenv(env_var)
            if not value:
                raise ValueError(f"Required environment variable {env_var} is not set")
            params[param_name] = value
        
        # Add optional parameters if available
        for param_name, env_var in optional_params.items():
            value = os.getenv(env_var)
            if value:
                params[param_name] = value
        
        # Add additional connection settings
        params.update({
            'client_session_keep_alive': True,
            'autocommit': True,
            'application': 'AutoGen_SnowflakeQueryTool'
        })
        
        return params
    
    def _create_connection(self):
        """
        Create a new Snowflake connection using the configured parameters.
        
        Returns:
            snowflake.connector.connection: Snowflake database connection
            
        Raises:
            Exception: If connection fails
        """
        try:
            self.logger.info("Creating Snowflake connection...")
            connection = snowflake.connector.connect(**self.connection_params)
            self.logger.info("Successfully connected to Snowflake")
            return connection
        except Exception as e:
            self.logger.error(f"Failed to connect to Snowflake: {str(e)}")
            raise
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections with automatic cleanup.
        
        Yields:
            snowflake.connector.connection: Database connection
        """
        connection = None
        try:
            connection = self._create_connection()
            yield connection
        except Exception as e:
            self.logger.error(f"Database connection error: {str(e)}")
            raise
        finally:
            if connection:
                try:
                    connection.close()
                    self.logger.info("Database connection closed")
                except Exception as e:
                    self.logger.warning(f"Error closing connection: {str(e)}")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Snowflake connection and return connection details.
        
        Returns:
            Dict[str, Any]: Connection test results
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT CURRENT_VERSION() as version, CURRENT_WAREHOUSE() as warehouse, CURRENT_DATABASE() as database, CURRENT_SCHEMA() as schema, CURRENT_ROLE() as role")
                result = cursor.fetchone()
                
                return {
                    "success": True,
                    "message": "Connection successful",
                    "details": {
                        "version": result[0],
                        "warehouse": result[1], 
                        "database": result[2],
                        "schema": result[3],
                        "role": result[4]
                    }
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "details": None
            }
    
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
        try:
            self.logger.info(f"Executing Snowflake query: {query}")
            if goal:
                self.logger.info(f"Query goal: {goal}")
            
            with self._get_connection() as conn:
                # Use DictCursor for easier data handling
                cursor = conn.cursor(DictCursor)
                cursor.execute(query)
                
                # Fetch results
                results = cursor.fetchall()
                
                # Convert to pandas DataFrame for easier manipulation
                if results:
                    df = pd.DataFrame(results)
                else:
                    df = pd.DataFrame()
                
                # Format return data based on requested format
                if return_format.lower() == "dataframe":
                    data = df
                elif return_format.lower() == "list":
                    data = results
                else:  # default to dict
                    data = df.to_dict('records') if not df.empty else []
                
                # Get query metadata
                row_count = len(results) if results else 0
                columns = list(df.columns) if not df.empty else []
                
                return {
                    "success": True,
                    "data": data,
                    "query": query,
                    "goal": goal,
                    "row_count": row_count,
                    "columns": columns,
                    "data_frame": df,
                    "return_format": return_format
                }
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Query execution failed: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "query": query,
                "goal": goal,
                "row_count": 0,
                "columns": [],
                "data": None,
                "return_format": return_format
            }
    
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
        try:
            # Build the query to get table information
            table_ref = table_name
            if schema:
                table_ref = f"{schema}.{table_name}"
            if database:
                table_ref = f"{database}.{table_ref}"
            
            # Query to get column information
            info_query = f"""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                ORDINAL_POSITION,
                COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table_name.upper()}'
            {f"AND TABLE_SCHEMA = '{schema.upper()}'" if schema else ""}
            {f"AND TABLE_CATALOG = '{database.upper()}'" if database else ""}
            ORDER BY ORDINAL_POSITION
            """
            
            result = self.execute_query(info_query, f"Get table information for {table_ref}")
            
            if result["success"]:
                return {
                    "success": True,
                    "table_name": table_name,
                    "schema": schema,
                    "database": database,
                    "columns": result["data"],
                    "column_count": result["row_count"]
                }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get table info: {str(e)}",
                "table_name": table_name
            }

    def list_tables(self, schema: str, database: str) -> Dict[str, Any]:
        """
        List all tables in the specified schema/database.
        
        Args:
            schema (str, optional): Schema name (uses current schema if not specified)
            database (str, optional): Database name (uses current database if not specified)
            
        Returns:
            Dict[str, Any]: List of tables with metadata
        """
        try:
            query = """
            SELECT 
                TABLE_CATALOG as DATABASE_NAME,
                TABLE_SCHEMA as SCHEMA_NAME,
                TABLE_NAME,
                TABLE_TYPE,
                ROW_COUNT,
                BYTES,
                COMMENT
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            """
            
            conditions = []
            if schema:
                conditions.append(f"TABLE_SCHEMA = '{schema.upper()}'")
            if database:
                conditions.append(f"TABLE_CATALOG = '{database.upper()}'")
            
            if conditions:
                query += " AND " + " AND ".join(conditions)
            
            query += " ORDER BY TABLE_SCHEMA, TABLE_NAME"
            
            result = self.execute_query(query, f"List tables in {schema or 'current schema'}")
            
            if result["success"]:
                return {
                    "success": True,
                    "tables": result["data"],
                    "table_count": result["row_count"],
                    "schema": schema,
                    "database": database
                }
            else:
                return result
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list tables: {str(e)}"
            }
