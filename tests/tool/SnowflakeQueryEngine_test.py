from agent.tool.SnowflakeQueryEngine import SnowflakeQueryEngine

if __name__ == "__main__":
    """
    Example usage of the SnowflakeQueryTool
    """
    try:
        # Create tool instance
        tool = SnowflakeQueryEngine()

        # Test connection
        print("Testing Snowflake connection...")
        connection_result = tool.test_connection()
        print(f"Connection test: {connection_result}")
        
        if connection_result["success"]:
            # Example query
            print("\nExecuting sample query...")
            query_result = tool.execute_query(
                "SELECT CURRENT_TIMESTAMP() as current_time, CURRENT_USER() as current_user",
                "Get current timestamp and user"
            )
            print(f"Query result: {query_result}")
            
            # List tables example
            print("\nListing tables...")
            tables_result = tool.list_tables()
            print(f"Tables: {tables_result}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have set the required environment variables:")
        print("- SNOWFLAKE_ACCOUNT (required)")
        print("- SNOWFLAKE_USER (required)")
        print("- SNOWFLAKE_TOKEN (PAT token - required)")
        print("\nOptional parameters:")
        print("- SNOWFLAKE_WAREHOUSE")
        print("- SNOWFLAKE_DATABASE")
        print("- SNOWFLAKE_SCHEMA")
        print("- SNOWFLAKE_ROLE")
        print("\nThis tool uses PAT token authentication only.")
        print("To get a PAT token:")
        print("1. Log into Snowflake web interface")
        print("2. Go to your user profile (top right)")
        print("3. Navigate to 'Personal Access Tokens'")
        print("4. Generate a new token")
        print("\nCreate a .env file based on .env.template for easy configuration.")