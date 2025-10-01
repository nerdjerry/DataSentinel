def create_snowflake_query_tool():
    """
    Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.execute_query method.
    
    Returns:
        FunctionTool: AutoGen tool for executing Snowflake queries
    """
    try:
        from autogen_core.tools import FunctionTool
        
        snowflake_instance = SnowflakeQueryTool()
        return FunctionTool(
            snowflake_instance.execute_query,
            description="Execute SQL queries on Snowflake database. Returns structured data with success status, results, and metadata."
        )
    except ImportError:
        raise ImportError("autogen-core is required. Install with: pip install autogen-core")


def create_snowflake_table_info_tool():
    """
    Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.get_table_info method.
    
    Returns:
        FunctionTool: AutoGen tool for getting table information
    """
    try:
        from autogen_core.tools import FunctionTool
        
        snowflake_instance = SnowflakeQueryTool()
        return FunctionTool(
            snowflake_instance.get_table_info,
            description="Get detailed information about a Snowflake table including column names, data types, and metadata."
        )
    except ImportError:
        raise ImportError("autogen-core is required. Install with: pip install autogen-core")


def create_snowflake_list_tables_tool():
    """
    Create an AutoGen FunctionTool wrapping the SnowflakeQueryTool.list_tables method.
    
    Returns:
        FunctionTool: AutoGen tool for listing tables
    """
    try:
        from autogen_core.tools import FunctionTool
        
        snowflake_instance = SnowflakeQueryTool()
        return FunctionTool(
            snowflake_instance.list_tables,
            description="List all tables in a Snowflake schema/database with metadata including row counts and table types."
        )
    except ImportError:
        raise ImportError("autogen-core is required. Install with: pip install autogen-core")