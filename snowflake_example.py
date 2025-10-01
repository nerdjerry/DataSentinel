"""
Example usage of the SnowflakeQueryTool with AutoGen agents

This example demonstrates how to:
1. Set up environment variables for Snowflake connection
2. Create a SnowflakeQueryTool instance
3. Wrap it in AutoGen FunctionTool
4. Use it with AutoGen agents for data analysis

from autogen_core.tools import FunctionTool
    from agent.tool.snowflake import SnowflakeQueryTool
    
    # Create the tool instance
    snowflake_tool_instance = SnowflakeQueryTool()
    
    # Wrap in AutoGen FunctionTool
    snowflake_tool = FunctionTool(
        snowflake_tool_instance.execute_query,
        description="Execute SQL queries on Snowflake database"
    )
    
    # Use with AutoGen agent
    agent = AssistantAgent(
        name="DataAgent",
        model_client=model_client,
        tools=[snowflake_tool],
        system_message="You are a data analyst with access to Snowflake database..."
    )

Prerequisites:
- Install required packages: pip install -r requirements-snowflake.txt
- Set up Snowflake environment variables
- Configure OpenAI API key for AutoGen agents
"""

import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agent.tool.snowflake import (
    create_snowflake_query_tool, 
    create_snowflake_table_info_tool, 
    create_snowflake_list_tables_tool,
    SnowflakeQueryTool
)


def setup_environment_variables():
    """
    Example function to set up Snowflake environment variables.
    In practice, these should be set in your shell environment or .env file.
    """
    # IMPORTANT: Replace these with your actual Snowflake credentials
    # DO NOT hardcode credentials in production code!
    
    example_env_vars = {
        'SNOWFLAKE_ACCOUNT': 'your_account.snowflakecomputing.com',
        'SNOWFLAKE_USER': 'your_username',
        'SNOWFLAKE_PASSWORD': 'your_password', 
        'SNOWFLAKE_WAREHOUSE': 'COMPUTE_WH',  # Optional
        'SNOWFLAKE_DATABASE': 'SAMPLE_DB',    # Optional
        'SNOWFLAKE_SCHEMA': 'PUBLIC',         # Optional
        'SNOWFLAKE_ROLE': 'SYSADMIN',        # Optional
        'OPENAI_API_KEY': 'your_openai_api_key'
    }
    
    print("Example environment variables (replace with your actual values):")
    for key, value in example_env_vars.items():
        print(f"export {key}='{value}'")
    
    print("\nMake sure to set these in your environment before running the script!")


async def example_basic_usage():
    """
    Example of basic SnowflakeQueryTool usage without AutoGen agents.
    """
    print("=== Basic Snowflake Tool Usage ===")
    
    try:
        # Create tool instance
        tool = SnowflakeQueryTool()
        
        # Test connection
        print("Testing Snowflake connection...")
        connection_result = tool.test_connection()
        print(f"Connection status: {connection_result['success']}")
        if connection_result['success']:
            print(f"Details: {connection_result['details']}")
        else:
            print(f"Error: {connection_result['message']}")
            return
        
        # Execute a simple query
        print("\nExecuting sample query...")
        result = tool.execute_query(
            "SELECT CURRENT_TIMESTAMP() as current_time, CURRENT_USER() as current_user, CURRENT_DATABASE() as database",
            "Get current session information"
        )
        
        if result['success']:
            print(f"Query returned {result['row_count']} rows")
            print(f"Data: {result['data']}")
        else:
            print(f"Query failed: {result['error']}")
            
        # List tables
        print("\nListing tables...")
        tables_result = tool.list_tables()
        if tables_result['success']:
            print(f"Found {tables_result['table_count']} tables")
            for table in tables_result['tables'][:5]:  # Show first 5 tables
                print(f"  - {table['SCHEMA_NAME']}.{table['TABLE_NAME']} ({table['ROW_COUNT']} rows)")
        else:
            print(f"Failed to list tables: {tables_result['error']}")
            
    except Exception as e:
        print(f"Error in basic usage: {e}")


async def example_autogen_agent_usage():
    """
    Example of using SnowflakeQueryTool with AutoGen agents.
    """
    print("\n=== AutoGen Agent with Snowflake Tool ===")
    
    try:
        # Create OpenAI model client
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        
        # Create Snowflake tools
        query_tool = create_snowflake_query_tool()
        table_info_tool = create_snowflake_table_info_tool()
        
        # Create AutoGen agent with Snowflake tools
        snowflake_agent = AssistantAgent(
            name="SnowflakeDataAgent",
            model_client=model_client,
            tools=[query_tool, table_info_tool],
            system_message="""You are a data analyst with access to a Snowflake database.
            
            Your responsibilities:
            1. Execute SQL queries to extract data for analysis
            2. Explore database structure and table schemas
            3. Provide insights based on query results
            4. Handle errors gracefully and suggest alternatives
            
            When querying:
            - Start with simple queries to understand the data structure
            - Use LIMIT clauses for exploratory queries
            - Explain what each query is trying to achieve
            - Focus on accuracy and clear data presentation
            
            Available tools:
            - execute_query: Run SQL queries against Snowflake
            - get_table_info: Get detailed information about specific tables
            """,
            reflect_on_tool_use=True
        )
        
        # Example tasks for the agent
        tasks = [
            "First, test the connection and show me what database and schema we're currently using.",
            "List all available tables in the current schema and show me the first few with row counts.",
            "Pick one interesting table and show me its structure including column names and data types.",
        ]
        
        for i, task in enumerate(tasks, 1):
            print(f"\n--- Task {i}: {task} ---")
            try:
                await Console(snowflake_agent.run_stream(task=task))
            except Exception as e:
                print(f"Task {i} failed: {e}")
                
    except Exception as e:
        print(f"Error in AutoGen usage: {e}")


async def example_data_analysis_workflow():
    """
    Example of a complete data analysis workflow using Snowflake with AutoGen.
    """
    print("\n=== Complete Data Analysis Workflow ===")
    
    try:
        # Create model client  
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        
        # Create comprehensive Snowflake agent
        analytics_agent = AssistantAgent(
            name="SnowflakeAnalyticsAgent", 
            model_client=model_client,
            tools=[
                create_snowflake_query_tool(),
                create_snowflake_table_info_tool(),
                create_snowflake_list_tables_tool()
            ],
            system_message="""You are a senior data analyst specializing in Snowflake analytics.
            
            Your workflow for data analysis:
            1. Explore available data sources and understand the schema
            2. Identify relevant tables for the analysis goal
            3. Execute exploratory queries to understand data quality and distribution
            4. Generate insights and recommendations based on findings
            5. Present results in a clear, business-friendly format
            
            Best practices:
            - Always start with small sample queries before running large operations
            - Use appropriate date filters and LIMIT clauses
            - Validate data quality and handle null values appropriately  
            - Provide context and business interpretation for your findings
            - Suggest follow-up analyses when relevant
            """,
            reflect_on_tool_use=True
        )
        
        # Run a comprehensive analysis task
        analysis_task = """
        Perform a comprehensive analysis of our database:
        
        1. First, identify what data sources are available
        2. Focus on any sales, customer, or transaction related tables
        3. For the most promising table:
           - Analyze data quality (null values, data types, date ranges)
           - Generate basic descriptive statistics 
           - Identify any obvious trends or patterns
           - Suggest 3 potential business insights we could derive
        
        Present your findings as a structured analysis report.
        """
        
        print("Starting comprehensive Snowflake analysis...")
        await Console(analytics_agent.run_stream(task=analysis_task))
        
    except Exception as e:
        print(f"Error in analysis workflow: {e}")


if __name__ == "__main__":
    """
    Main execution block - demonstrates different usage patterns
    """
    import asyncio
    
    print("Snowflake AutoGen Integration Examples")
    print("=" * 50)
    
    # Check if environment variables are set
    required_vars = ['SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {missing_vars}")
        setup_environment_variables()
        print("\nPlease set the environment variables and run again.")
        exit(1)
    
    # Run examples
    async def run_all_examples():
        try:
            await example_basic_usage()
            
            if os.getenv('OPENAI_API_KEY'):
                await example_autogen_agent_usage()
                await example_data_analysis_workflow()
            else:
                print("\nSkipping AutoGen examples - OPENAI_API_KEY not set")
                
        except KeyboardInterrupt:
            print("\nExecution interrupted by user")
        except Exception as e:
            print(f"Error running examples: {e}")
    
    # Run the examples
    asyncio.run(run_all_examples())