# DataSentinel Architecture with Great Expectations Integration

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DataSentinel Platform                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         Agent Layer                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  DataAgent   │  │DataQuality   │  │ DataProfiling        │   │
│  │              │  │Agent         │  │ Agent                │   │
│  │  - Query DB  │  │              │  │                      │   │
│  │  - Analyze   │  │ - Assess     │  │ - Profile with yp    │   │
│  │  - Uber Data │  │ - Quality    │  │ - Generate Reports   │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────────┘   │
│         │                 │                  │                  │
└─────────┼─────────────────┼──────────────────┼──────────────────┘
          │                 │                  │
          │                 │                  │
┌─────────┼─────────────────┼──────────────────┼──────────────────┐
│         │    Model Layer  │                  │                  │
├─────────┼─────────────────┼──────────────────┼──────────────────┤
│         │                 │                  │                  │
│         └─────────────────┴──────────────────┘                  │
│                           │                                     |
│                  ┌────────▼────────┐                            │
│                  │  ModelFactory   │                            │
│                  │                 │                            │
│                  │  - OpenAI       │                            │
│                  │  - API Key Mgmt │                            │
│                  └─────────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        Tool Factory Layer                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐        ┌─────────────────────────────┐ │
│  │ SnowflakeQuery       │        │ SnowflakeDataProfiling      │ │
│  │ ToolFactory          │        │ ToolFactory                 │ │
│  │                      │        │                             │ │
│  │ - create_query_tool()│        │ - create_profile_tool()     │ │
│  │ - create_table_info()│        │ - create_connection_test()  │ │
│  │ - create_list_tables │        │                             │ │
│  └──────────┬───────────┘        └─────────────┬───────────────┘ │
│             │                                   │                │
└─────────────┼───────────────────────────────────┼────────────────┘
              │                                   │
              │                                   │
┌─────────────┼───────────────────────────────────┼────────────────┐
│             │       Tool Layer                  │                │
├─────────────┼───────────────────────────────────┼────────────────┤
│             │                                   │                │
│  ┌──────────▼──────────┐          ┌────────────▼──────────────┐  │
│  │ SnowflakeQuery      │          │ SnowflakeDataProfiling    │  │
│  │ Engine              │          │ Tool                      │  │
│  │                     │          │                           │  │
│  │ - execute_query()   │◄─────────┤ Uses for query execution  │  │
│  │ - get_table_info()  │          │                           │  │
│  │ - list_tables()     │          │ - profile_data()          │  │
│  │ - test_connection() │          │ - test_connection()       │  │
│  └──────────┬──────────┘          │ - generate_html_report()  │  │
│             │                     │ - generate_json_report()  │  │
│             │                     └────────────┬──────────────┘  │
│             │                                  │                 │
└─────────────┼──────────────────────────────────┼─────────────────┘
              │                                  │
              │                                  │
┌─────────────┼──────────────────────────────────┼────────────────┐
│             │    External Services             │                │
├─────────────┼──────────────────────────────────┼────────────────┤
│             │                                  │                │
│  ┌──────────▼──────────┐          ┌───────────▼──────────────┐  │
│  │   Snowflake         │          │  ydata-profiling.        │  │
│  │   Database          │          │                          │  │
│  │                     │          │  - DataContext           │  │
│  │  - RIDEBOOKING      │          │  - Profiler              │  │
│  │  - Tables/Views     │          │  - Expectations          │  │
│  │  - Schemas          │          │  - Validators            │  │
│  └─────────────────────┘          │  - Report Generation     │  │
│                                   └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                        Output Layer                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  Query Results    │  │  HTML Reports    │  │  JSON Reports │  │
│  │                   │  │                  │  │               │  │
│  │  - Tabular Data   │  │  - Visual        │  │  - Metrics    │  │
│  │  - Pandas DF      │  │  - Interactive   │  │  - Statistics │  │
│  │  - JSON/Dict      │  │  - Expectations  │  │  - Quality    │  │
│  └───────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow for Profiling

```
User Request
    │
    ▼
┌───────────────────────────────────────────┐
│ "Profile RIDEBOOKING table"               │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ DataProfilingAgent                        │
│ - Interprets request                      │
│ - Constructs SQL query                    │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ SnowflakeDataProfilingTool                │
│ - Receives query                          │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ SnowflakeQueryEngine                      │
│ - Executes query                          │
│ - Returns DataFrame                       │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ ydata-profiling.                          │
│ - Creates batch from DataFrame            │
│ - Profiles dataset                        │
│ - Generates expectations                  │
│ - Validates data                          │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Metrics Extraction                        │
│ - Basic stats (rows, columns, memory)     │
│ - Column metrics (nulls, uniques, types)  │
│ - Data quality (pass/fail rates)          │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ Report Generation                         │
│ - HTML: Visual representation             │
│ - JSON: Programmatic access               │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ DataProfilingAgent                        │
│ - Summarizes results                      │
│ - Highlights issues                       │
│ - Provides recommendations                │
└───────────────┬───────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────┐
│ User Response                             │
│ - Summary of profiling                    │
│ - Key findings                            │
│ - Report file paths                       │
└───────────────────────────────────────────┘
```

## Component Interactions

### Query Execution Path
```
DataAgent → SnowflakeQueryToolFactory → SnowflakeQueryEngine → Snowflake DB
```

### Profiling Execution Path
```
DataProfilingAgent → SnowflakeDataProfilingFactory 
                  → SnowflakeDataProfilingTool
                  → SnowflakeQueryEngine → Snowflake DB
                  → Great Expectations → Reports
```

### Quality Assessment Path
```
DataQualityAgent → DataAgent (for data retrieval)
                → Analysis & Recommendations
```

## File Structure

```
DataSentinel/
├── agent/
│   ├── DataAgent.py                         # SQL query agent
│   ├── DataQualityAgent.py                  # Quality assessment agent
│   ├── DataProfilingAgent.py               # NEW: Profiling agent
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   └── ModelFactory.py                  # OpenAI client factory
│   │
│   ├── tool/
│   │   ├── __init__.py
│   │   ├── SnowflakeQueryEngine.py         # Query execution
│   │   ├── SnowflakeQueryToolFactory.py    # Query tool factory
│   │   ├── SnowflakeDataProfilingTool.py       # NEW: tool
│   │   ├── SnowflakeDataProfilingToolFactory.py # NEW:  factory
│   │   ├── SnowflakeQueryEngine_test.py
│   │   └── SnowflakeDataProfilingTool_test.py  # NEW: Test
│   │
│   └── unittest/
│       ├── DataAgent_test.py
│       ├── DataQualityAgent_test.py
│       └── DataProfilingAgent_test.py      # NEW: Agent test
│
├── ge_reports/                              # NEW: Generated reports
│   ├── *.html                              # Visual reports
│   └── *.json                              # Metrics reports
│
├── requirements.txt                         # Dependencies
├── README_Snowflake.md                     # Main docs
├── README_YDataprofiling.md            # NEW: GE docs
└── IMPLEMENTATION_SUMMARY.md              # NEW: Summary
```

## Technology Stack

### Core Technologies
- **Python 3.10+**: Programming language
- **AutoGen**: Multi-agent framework
- **YData Profiling**: Data profiling
- **Snowflake**: Cloud data warehouse
- **Pandas**: Data manipulation
- **OpenAI GPT**: Language models

### Key Libraries
```
autogen-core>=0.7.0
autogen-agentchat>=0.7.0
autogen-ext[openai]
snowflake-connector-python>=3.12.0
ydata-profiling>=0.18.0
sqlalchemy-snowflake>=1.5.0
pandas>=1.5.0
python-dotenv
```

## Environment Configuration

```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=YOUR_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=SYSADMIN

# AI Model
OPENAI_API_KEY=your_openai_api_key
```

## Security Architecture

```
┌─────────────────────────────────────┐
│     Environment Variables           │
│  - No hardcoded credentials         │
│  - .env file support                │
│  - OS environment variables         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     Connection Management           │
│  - Context managers                 │
│  - Automatic cleanup                │
│  - Connection pooling               │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     Secure Communication            │
│  - Encrypted connections            │
│  - Token-based auth support         │
│  - Role-based access control        │
└─────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- Multiple agent instances
- Parallel profiling tasks
- Distributed report generation

### Vertical Scaling
- Adjustable warehouse sizes in Snowflake
- Memory-efficient data processing
- Streaming for large datasets

### Performance Optimization
- Query result caching
- Incremental profiling
- Selective column analysis
- Row sampling strategies
