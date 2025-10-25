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
        # TODO: Implement this method
        # 1. Create and return a FunctionTool instance
        # 2. Use self.snowflake_instance.execute_query as the function
        # 3. Add appropriate description for the tool
        # 4. Set strict=True for type checking
        # 5. Handle ImportError if autogen-core is not installed
        pass

    def create_table_info_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.get_table_info method.

        Returns:
            FunctionTool: AutoGen tool for getting table information
        """
        # TODO: Implement this method
        # 1. Create and return a FunctionTool instance
        # 2. Use self.snowflake_instance.get_table_info as the function
        # 3. Add description about getting table metadata
        # 4. Set strict=True for type checking
        # 5. Handle ImportError if autogen-core is not installed
        pass

    def create_list_tables_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.list_tables method.

        Returns:
            FunctionTool: AutoGen tool for listing tables
        """
        # TODO: Implement this method
        # 1. Create and return a FunctionTool instance
        # 2. Use self.snowflake_instance.list_tables as the function
        # 3. Add description about listing tables in schema/database
        # 4. Set strict=True for type checking
        # 5. Handle ImportError if autogen-core is not installed
        pass
