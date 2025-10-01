# Snowflake Integration for AutoGen Agents

This module provides a comprehensive Snowflake database integration for AutoGen agents, allowing AI agents to connect to and query Snowflake databases seamlessly.

## Features

- **Secure Connection Management**: Uses environment variables for credentials
- **AutoGen Integration**: Ready-to-use FunctionTool wrappers
- **Comprehensive Query Support**: Execute any SQL query with error handling
- **Schema Exploration**: Built-in tools for table discovery and schema inspection
- **Connection Pooling**: Efficient connection management with context managers
- **Multiple Return Formats**: Support for pandas DataFrames, dictionaries, and lists

## Installation

1. Install required dependencies:
```bash
pip install -r requirements-snowflake.txt
```

2. Set up your Snowflake environment variables:
```bash
export SNOWFLAKE_ACCOUNT='your_account.snowflakecomputing.com'
export SNOWFLAKE_USER='your_username'  
export SNOWFLAKE_PASSWORD='your_password'
export SNOWFLAKE_WAREHOUSE='COMPUTE_WH'  # Optional
export SNOWFLAKE_DATABASE='YOUR_DB'      # Optional  
export SNOWFLAKE_SCHEMA='PUBLIC'         # Optional
export SNOWFLAKE_ROLE='SYSADMIN'        # Optional
```

3. For AutoGen integration, also set:
```bash
export OPENAI_API_KEY='your_openai_api_key'
```

## Quick Start

### Basic Usage

```python
from agent.tool.snowflake import SnowflakeQueryTool

# Create tool instance
tool = SnowflakeQueryTool()

# Test connection
result = tool.test_connection()
print(f"Connection: {result['success']}")

# Execute query
query_result = tool.execute_query(
    "SELECT COUNT(*) as total_rows FROM your_table",
    "Get total row count"
)

if query_result['success']:
    print(f"Data: {query_result['data']}")
```

### AutoGen Agent Integration

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agent.tool.snowflake import create_snowflake_query_tool

# Create model client
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Create Snowflake tool
snowflake_tool = create_snowflake_query_tool()

# Create agent with Snowflake access
agent = AssistantAgent(
    name="DataAnalyst",
    model_client=model_client,
    tools=[snowflake_tool],
    system_message="You are a data analyst with access to Snowflake database..."
)

# Use the agent
await agent.run_stream(task="Analyze sales data for the last quarter")
```

## Available Tools

### 1. SnowflakeQueryTool
Main class providing Snowflake database operations.

**Methods:**
- `execute_query(query, goal, return_format)`: Execute SQL queries
- `test_connection()`: Test database connectivity
- `get_table_info(table_name, schema, database)`: Get table schema details
- `list_tables(schema, database)`: List available tables

### 2. AutoGen Function Tools
Pre-configured tools for AutoGen integration:

- `create_snowflake_query_tool()`: SQL query execution
- `create_snowflake_table_info_tool()`: Table schema inspection  
- `create_snowflake_list_tables_tool()`: Table discovery

## Examples

Run the comprehensive example:
```bash
python snowflake_example.py
```

This demonstrates:
- Basic Snowflake operations
- AutoGen agent integration
- Complete data analysis workflows

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Yes | Snowflake account identifier |
| `SNOWFLAKE_USER` | Yes | Username for authentication |
| `SNOWFLAKE_PASSWORD` | Yes | Password for authentication |
| `SNOWFLAKE_WAREHOUSE` | No | Default warehouse to use |
| `SNOWFLAKE_DATABASE` | No | Default database to use |
| `SNOWFLAKE_SCHEMA` | No | Default schema to use |
| `SNOWFLAKE_ROLE` | No | Role for the session |

## Security Best Practices

1. **Never hardcode credentials** in your source code
2. **Use environment variables** or secure credential management systems
3. **Limit database permissions** to only what's needed for your use case
4. **Use appropriate Snowflake roles** with minimal required privileges
5. **Monitor query costs** and set up resource monitors in Snowflake

## Error Handling

The tool provides comprehensive error handling:
- Connection failures are caught and reported
- SQL syntax errors are returned with context
- Query timeouts are handled gracefully
- Resource exhaustion is detected and reported

## Integration with Existing Codebase

This Snowflake tool follows the same patterns as the existing SQLite tool in your codebase:

```python
# Similar to existing SQL tool pattern
sql_tool = FunctionTool(execute_sql_query, description="Execute SQL queries on the sales database")

# Now with Snowflake
snowflake_tool = create_snowflake_query_tool()

# Both can be used with the same agent patterns
data_agent = AssistantAgent(
    name="DataAgent",
    model_client=model_client,
    tools=[sql_tool, snowflake_tool],  # Multiple database support
    system_message="You have access to both SQLite and Snowflake databases..."
)
```

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check your environment variables and network connectivity
2. **Authentication Error**: Verify username/password and account identifier
3. **Permission Denied**: Ensure your user has appropriate database/schema permissions
4. **Import Errors**: Install required packages with `pip install -r requirements-snowflake.txt`

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Considerations

- Use `LIMIT` clauses for exploratory queries
- Consider query costs in Snowflake (credits consumed)
- Use appropriate warehouse sizes for your workload
- Cache results when possible to avoid repeated queries

## Contributing

When extending this module:
1. Follow the existing error handling patterns
2. Add comprehensive docstrings
3. Include type hints
4. Test with various Snowflake configurations
5. Update this README with new features