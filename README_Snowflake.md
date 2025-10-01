# DataSentinel - AI-Powered Data Analysis Platform

DataSentinel is an intelligent data analysis platform that combines AutoGen AI agents with Snowflake database connectivity to provide automated data querying and quality analysis capabilities.

## Features

- **Multi-Agent Architecture**: Specialized agents for data querying and quality analysis
- **Snowflake Integration**: Secure connection management with Personal Access Token (PAT) authentication
- **Intelligent Data Analysis**: AI-powered data quality assessment and anomaly detection  
- **AutoGen Framework**: Built on Microsoft's AutoGen multi-agent framework
- **Comprehensive Query Support**: Execute any SQL query with error handling and result formatting
- **Schema Discovery**: Built-in tools for table discovery and schema inspection
- **Quality Assessment**: Automated data quality checks including missing values, duplicates, and outliers

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Snowflake environment variables:
```bash
export SNOWFLAKE_ACCOUNT='your_account.snowflakecomputing.com'
export SNOWFLAKE_USER='your_username'  
export SNOWFLAKE_PASSWORD='your_password'  # Or use PAT token
export SNOWFLAKE_WAREHOUSE='COMPUTE_WH'     # Optional
export SNOWFLAKE_DATABASE='YOUR_DB'         # Optional  
export SNOWFLAKE_SCHEMA='PUBLIC'            # Optional
export SNOWFLAKE_ROLE='SYSADMIN'           # Optional
```

3. Set up OpenAI API key for AI agents:
```bash
export OPENAI_API_KEY='your_openai_api_key'
```

4. (Optional) Create a `.env` file in the project root with your environment variables for local development.

## Quick Start

### Using the DataAgent

```python
import asyncio
from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent

async def main():
    # Create a DataAgent instance
    data_agent = DataAgent().get_agent()
    
    # Run a data analysis task
    await Console(data_agent.run_stream(task="Get top 10 rows from the RIDEBOOKING table"))

asyncio.run(main())
```

### Using the DataQualityAgent

```python
import asyncio
from autogen_agentchat.ui import Console
from agent.DataQualityAgent import DataQualityAgent

async def main():
    # Create a DataQualityAgent instance
    quality_agent = DataQualityAgent().get_agent()
    
    # Run a data quality assessment
    await Console(quality_agent.run_stream(task="Analyze data quality issues in the RIDEBOOKING table"))

asyncio.run(main())
```

### Direct Snowflake Query Engine Usage

```python
from agent.tool.SnowflakeQueryEngine import SnowflakeQueryEngine

# Create query engine instance
engine = SnowflakeQueryEngine()

# Test connection
result = engine.test_connection()
print(f"Connection: {result['success']}")

# Execute query
query_result = engine.execute_query(
    "SELECT COUNT(*) as total_rows FROM RIDEBOOKING",
    "Get total row count"
)

if query_result['success']:
    print(f"Data: {query_result['data']}")
```

## Architecture

### Agents

#### 1. DataAgent (`agent/DataAgent.py`)
Specialized agent for data querying and analysis with direct access to Snowflake.

**Capabilities:**
- Translates English business questions into SQL queries
- Executes queries against Snowflake databases
- Returns structured tabular results
- Focuses on Uber trip data analysis

**System Prompt:** Configured to handle table discovery, schema analysis, and accurate SQL query generation.

#### 2. DataQualityAgent (`agent/DataQualityAgent.py`)  
Specialized agent for comprehensive data quality assessment.

**Capabilities:**
- Detects missing values and null patterns
- Identifies data type mismatches and distribution anomalies
- Spots duplicates and referential integrity issues
- Finds outliers and inconsistent formats
- Provides actionable remediation recommendations

**Workflow:** Always collaborates with DataAgent to retrieve data before performing analysis.

### Core Components

#### 1. SnowflakeQueryEngine (`agent/tool/SnowflakeQueryEngine.py`)
Main query execution engine with comprehensive Snowflake operations.

**Methods:**
- `execute_query(query, goal, return_format)`: Execute SQL queries with multiple return formats
- `test_connection()`: Test database connectivity and retrieve connection details
- `get_table_info(table_name, schema, database)`: Get detailed table schema information
- `list_tables(schema, database)`: List available tables with metadata

#### 2. SnowflakeQueryToolFactory (`agent/tool/SnowflakeQueryToolFactory.py`)
Factory class that creates AutoGen-compatible function tools from the query engine.

#### 3. ModelFactory (`agent/model/ModelFactory.py`)
Centralized factory for creating OpenAI model clients with environment-based configuration.

## Usage Examples

### Run DataAgent Test
```bash
cd agent/unittest
python DataAgent_test.py
```

### Run DataQualityAgent Test
```bash
cd agent/unittest  
python DataQualityAgent_test.py
```

### Test Snowflake Connection
```bash
cd agent/tool
python SnowflakeQueryEngine_test.py
```

### Example Queries

**Data Analysis with DataAgent:**
- "Get top 10 rows from RIDEBOOKING table"
- "Show me the count of trips by pickup location"
- "What is the average trip duration in the last month?"

**Data Quality Analysis with DataQualityAgent:**
- "Analyze data quality issues in the RIDEBOOKING table"
- "Check for missing values and duplicates in trip data" 
- "Identify any anomalies in the fare amounts"

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SNOWFLAKE_ACCOUNT` | Yes | Snowflake account identifier |
| `SNOWFLAKE_USER` | Yes | Username for authentication |
| `SNOWFLAKE_PASSWORD` | Yes | Password or Personal Access Token (PAT) |
| `OPENAI_API_KEY` | Yes | OpenAI API key for AI agents |
| `SNOWFLAKE_WAREHOUSE` | No | Default warehouse to use |
| `SNOWFLAKE_DATABASE` | No | Default database to use |
| `SNOWFLAKE_SCHEMA` | No | Default schema to use |
| `SNOWFLAKE_ROLE` | No | Role for the session |

## Project Structure

```
DataSentinel/
├── app.py                           # Main application entry point
├── requirements.txt                 # Python dependencies
├── README_Snowflake.md             # This documentation
├── agent/
│   ├── DataAgent.py                # Data querying agent
│   ├── DataQualityAgent.py         # Data quality analysis agent
│   ├── model/
│   │   ├── __init__.py
│   │   └── ModelFactory.py         # OpenAI model client factory
│   ├── tool/
│   │   ├── __init__.py
│   │   ├── SnowflakeQueryEngine.py    # Core Snowflake query engine
│   │   ├── SnowflakeQueryEngine_test.py
│   │   └── SnowflakeQueryToolFactory.py # AutoGen tool factory
│   └── unittest/
│       ├── DataAgent_test.py        # DataAgent test script
│       └── DataQualityAgent_test.py # DataQualityAgent test script
```

## Security Best Practices

1. **Never hardcode credentials** in your source code
2. **Use environment variables** or `.env` files for credential management
3. **Consider using Personal Access Tokens (PAT)** instead of passwords for enhanced security
4. **Limit database permissions** to only what's needed for your use case
5. **Use appropriate Snowflake roles** with minimal required privileges
6. **Monitor query costs** and set up resource monitors in Snowflake
7. **Keep API keys secure** and rotate them regularly

## Error Handling

The tool provides comprehensive error handling:
- Connection failures are caught and reported
- SQL syntax errors are returned with context
- Query timeouts are handled gracefully
- Resource exhaustion is detected and reported

## Agent Collaboration

The DataSentinel platform is designed for multi-agent collaboration:

```python
import asyncio
from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent
from agent.DataQualityAgent import DataQualityAgent

async def collaborative_analysis():
    # Create both agents
    data_agent = DataAgent().get_agent()
    quality_agent = DataQualityAgent().get_agent()
    
    # DataAgent first retrieves and analyzes data
    data_task = "Get a sample of 1000 rows from RIDEBOOKING table"
    
    # DataQualityAgent then assesses the quality
    quality_task = "Analyze the data quality of the retrieved RIDEBOOKING data"
    
    # Agents can work together through the Console interface
    await Console([data_agent, quality_agent]).run_stream(
        task="Perform comprehensive data analysis including quality assessment"
    )

asyncio.run(collaborative_analysis())
```

## Troubleshooting

### Common Issues

1. **Connection Failed**: 
   - Check your environment variables and network connectivity
   - Verify Snowflake account identifier format
   - Test connection using `SnowflakeQueryEngine_test.py`

2. **Authentication Error**: 
   - Verify username/password or PAT token
   - Check account identifier and user permissions
   - Ensure credentials are correctly set in environment

3. **Permission Denied**: 
   - Ensure your user has appropriate database/schema permissions
   - Check if the specified warehouse, database, and schema exist
   - Verify role permissions for the resources you're trying to access

4. **Import Errors**: 
   - Install required packages with `pip install -r requirements.txt`
   - Verify Python version compatibility
   - Check if all AutoGen dependencies are correctly installed

5. **Agent Errors**:
   - Ensure `OPENAI_API_KEY` is set correctly
   - Verify model availability (default is "gpt-5-mini")
   - Check agent system prompts and tool configurations

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Individual Components

```bash
# Test Snowflake connection
cd agent/tool
python SnowflakeQueryEngine_test.py

# Test DataAgent
cd agent/unittest
python DataAgent_test.py

# Test DataQualityAgent  
cd agent/unittest
python DataQualityAgent_test.py
```

## Performance Considerations

- **Query Optimization**: Use `LIMIT` clauses for exploratory queries to avoid large result sets
- **Cost Management**: Monitor Snowflake credits consumption, especially with AI agents that may generate multiple queries
- **Warehouse Sizing**: Use appropriate warehouse sizes for your workload complexity
- **Result Caching**: Cache results when possible to avoid repeated queries
- **Agent Efficiency**: DataQualityAgent is designed to request specific, minimal queries from DataAgent
- **Connection Management**: Query engine uses context managers for efficient connection handling
- **Return Formats**: Choose appropriate return formats (dict, dataframe, list) based on your use case

## Contributing

When extending DataSentinel:

### Code Standards
1. Follow the existing error handling patterns in `SnowflakeQueryEngine`
2. Add comprehensive docstrings and type hints
3. Use the factory pattern for creating new tools and models
4. Test with various Snowflake configurations

### Adding New Agents
1. Create new agent classes in the `agent/` directory
2. Follow the pattern established by `DataAgent` and `DataQualityAgent`
3. Use `ModelFactory` for consistent model client creation
4. Add corresponding test files in `agent/unittest/`

### Extending Tools
1. Add new query tools in `agent/tool/` directory
2. Use `SnowflakeQueryToolFactory` pattern for AutoGen integration
3. Include comprehensive error handling and logging
4. Add unit tests for new functionality

### Documentation
1. Update this README with new features and capabilities
2. Include example usage for new components
3. Document any new environment variables or configuration options
4. Add troubleshooting guidance for new features

## License

This project follows standard open-source practices. Please ensure any contributions maintain compatibility with existing dependencies and licensing requirements.