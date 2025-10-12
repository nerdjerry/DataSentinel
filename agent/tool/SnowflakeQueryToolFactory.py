from agent.tool.SnowflakeQueryEngine import SnowflakeQueryEngine
from autogen_core.tools import FunctionTool

class SnowflakeQueryToolFactory:
    """
    Factory class to create AutoGen FunctionTools for SnowflakeQueryTool methods.
    """
    def __init__(self):
        self.snowflake_instance = SnowflakeQueryEngine()

    def create_query_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.execute_query method.

        Returns:
            FunctionTool: AutoGen tool for executing Snowflake queries
        """
        try:
            return FunctionTool(
                self.snowflake_instance.execute_query,
                description="Execute SQL queries on Snowflake database. Returns structured data with success status, results, and metadata."
            )
        except ImportError:
            raise ImportError("autogen-core is required. Install with: pip install autogen-core")

    def create_table_info_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.get_table_info method.

        Returns:
            FunctionTool: AutoGen tool for getting table information
        """
        try:
            return FunctionTool(
                self.snowflake_instance.get_table_info,
                description="Get detailed information about a Snowflake table including column names, data types, and metadata."
            )
        except ImportError:
            raise ImportError("autogen-core is required. Install with: pip install autogen-core")

    def create_list_tables_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.list_tables method.

        Returns:
            FunctionTool: AutoGen tool for listing tables
        """
        try:
            return FunctionTool(
                self.snowflake_instance.list_tables,
                description="List all tables in a Snowflake schema/database with metadata including row counts and table types."
            )
        except ImportError:
            raise ImportError("autogen-core is required. Install with: pip install autogen-core")