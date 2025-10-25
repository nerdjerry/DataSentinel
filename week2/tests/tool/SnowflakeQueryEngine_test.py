import sys
from pathlib import Path
from agent.tool.SnowflakeQueryEngine import SnowflakeQueryEngine

if __name__ == "__main__":
    """
    Example usage of the SnowflakeQueryTool
    
    TODO: Students should implement the following:
    1. Create a SnowflakeQueryEngine instance
    2. Test the connection to Snowflake
    3. Execute a sample query to get current timestamp and user
    4. List available tables in the database
    5. Handle any exceptions and provide helpful error messages
    """
    
    # TODO: Implement the following steps
    
    # Step 1: Create tool instance
    # Hint: tool = SnowflakeQueryEngine()
    
    # Step 2: Test connection
    # Hint: Use tool.test_connection() and print the result
    
    # Step 3: If connection is successful, execute a sample query
    # Hint: Use tool.execute_query() with a SELECT statement
    # Example query: "SELECT CURRENT_TIMESTAMP() as current_time, CURRENT_USER() as current_user"
    
    # Step 4: List tables in the database
    # Hint: Use tool.list_tables() and print the result
    
    # Step 5: Handle exceptions
    # Hint: Wrap your code in try-except block
    # Provide helpful error messages about required environment variables:
    # - SNOWFLAKE_ACCOUNT (required)
    # - SNOWFLAKE_USER (required)
    # - SNOWFLAKE_TOKEN (PAT token - required)
    # Optional: SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, SNOWFLAKE_ROLE
    
    pass  # Remove this line when implementing
