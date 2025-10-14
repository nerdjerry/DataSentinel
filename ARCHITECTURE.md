# DataSentinel Architecture

## System Overview

DataSentinel is a multi-agent orchestration platform for comprehensive data quality analysis. It uses AutoGen's agent framework to coordinate specialized agents that work together to investigate, profile, analyze, and report on data quality issues in Snowflake databases.

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     DataSentinel Orchestrator                    │
│               (Multi-Phase Workflow Coordination)                │
└──────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│  Phase 1:    │      │  Phase 2:    │     │  Phase 3:    │
│  Planning    │─────▶│ Investigation│────▶│  Analysis    │
└──────────────┘      └──────────────┘     └──────┬───────┘
                                                   │
                                                   ▼
                                          ┌──────────────┐
                                          │  Phase 4:    │
                                          │  Reporting   │
                                          └──────────────┘
```

## Detailed Agent Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR LAYER                          │
│                        (Workflow Coordinator)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Orchestrator.py                                                    │
│  - Coordinates 4-phase workflow                                     │
│  - Manages agent communication via RoundRobinGroupChat              │
│  - Handles structured outputs (Pydantic models)                     │
│  - Saves reports and results                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ PHASE 1: PLANNING                                           │   │
│  │ ┌─────────────────────────────────────────────────────────┐ │   │
│  │ │ PlannerAgent                                            │ │   │
│  │ │ - Input: Data quality goal + schema                     │ │   │
│  │ │ - Output: DataQualityPlan                               │ │   │
│  │ │   • QueryTask[] for DataAgent                           │ │   │
│  │ │   • ProfilingTask[] for DataProfilingAgent              │ │   │
│  │ │   • execution_sequence[]                                │ │   │
│  │ │   • success_criteria[]                                  │ │   │
│  │ └─────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ PHASE 2: INVESTIGATION                                      │   │
│  │ ┌────────────────────┐      ┌──────────────────────────┐   │   │
│  │ │ DataAgent          │      │ DataProfilingAgent       │   │   │
│  │ │ - SQL queries      │      │ - ydata-profiling        │   │   │
│  │ │ - Evidence         │      │ - Statistical analysis   │   │   │
│  │ │   gathering        │      │ - HTML/JSON reports      │   │   │
│  │ │ - Tools:           │      │ - Tools:                 │   │   │
│  │ │   • query_tool     │      │   • profile_tool         │   │   │
│  │ │   • table_info     │      │   • (uses query_engine)  │   │   │
│  │ │   • list_tables    │      │                          │   │   │
│  │ │ - Output:          │      │ - Output:                │   │   │
│  │ │   DataAgentReport  │      │   DataProfilingReport    │   │   │
│  │ └────────────────────┘      └──────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ PHASE 3: ANALYSIS                                           │   │
│  │ ┌─────────────────────────────────────────────────────────┐ │   │
│  │ │ SummarizerAgent                                         │ │   │
│  │ │ - Correlates DataAgent + DataProfilingAgent results     │ │   │
│  │ │ - Identifies data quality issues                        │ │   │
│  │ │ - Assigns severity levels                               │ │   │
│  │ │ - Provides recommendations                              │ │   │
│  │ │ - Tools:                                                │ │   │
│  │ │   • read_profiling_report (to parse JSON profiles)      │ │   │
│  │ │ - Output: DataQualityAgentReport                        │ │   │
│  │ │   • summary                                             │ │   │
│  │ │   • issues[]                                            │ │   │
│  │ │   • recommendations[]                                   │ │   │
│  │ │   • required_followup_queries[]                         │ │   │
│  │ └─────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ PHASE 4: REPORTING                                          │   │
│  │ ┌─────────────────────────────────────────────────────────┐ │   │
│  │ │ ReportAgent                                             │ │   │
│  │ │ - Generates professional HTML report                    │ │   │
│  │ │ - Formats all findings                                  │ │   │
│  │ │ - Includes visualizations and links                     │ │   │
│  │ │ - Output: ReportResponse                                │ │   │
│  │ │   • html (complete report)                              │ │   │
│  │ │   • thoughts                                            │ │   │
│  │ └─────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          MODEL LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ ModelFactory                                                  │  │
│  │ - Creates OpenAI client instances                             │  │
│  │ - Model: gpt-4o-mini (default)                                │  │
│  │ - Configurable temperature (when supported)                   │  │
│  │ - API key management via environment variables                │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       TOOL FACTORY LAYER                            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌────────────────────────────────┐  │
│  │ SnowflakeQuery           │  │ SnowflakeDataProfiling         │  │
│  │ ToolFactory              │  │ ToolFactory                    │  │
│  │                          │  │                                │  │
│  │ - create_query_tool()    │  │ - create_profile_tool()        │  │
│  │ - create_table_info()    │  │                                │  │
│  │ - create_list_tables()   │  │                                │  │
│  └──────────┬───────────────┘  └────────────┬───────────────────┘  │
│             │                               │                      │
│  ┌──────────┴───────────────┐  ┌────────────┴───────────────────┐  │
│  │ ProfilingReportReader    │  │                                │  │
│  │ ToolFactory              │  │                                │  │
│  │                          │  │                                │  │
│  │ - create_read_tool()     │  │                                │  │
│  └──────────────────────────┘  └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           TOOL LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ SnowflakeQueryEngine                                        │   │
│  │ - execute_query() → DataFrame/JSON/Dict                     │   │
│  │ - get_table_info() → Schema information                     │   │
│  │ - list_tables() → Available tables                          │   │
│  │ - test_connection() → Connection validation                 │   │
│  └─────────────────────┬───────────────────────────────────────┘   │
│                        │                                            │
│  ┌─────────────────────▼───────────────────────────────────────┐   │
│  │ SnowflakeDataProfilingTool                                  │   │
│  │ - profile_data() → Statistical profile                      │   │
│  │ - Uses SnowflakeQueryEngine for data retrieval              │   │
│  │ - Uses ydata-profiling for analysis                         │   │
│  │ - Generates HTML/JSON reports                               │   │
│  │ - Configures matplotlib backend (Agg) for threading safety  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ProfilingReportReaderTool                                   │   │
│  │ - read_profiling_report() → Parses JSON profiling reports   │   │
│  │ - Extracts metrics, statistics, correlations                │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES LAYER                         │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐         ┌───────────────────────────┐    │
│  │ Snowflake Database   │         │ ydata-profiling           │    │
│  │ - RIDEBOOKING table  │         │ - ProfileReport           │    │
│  │ - Tables/Views       │         │ - Statistical analysis    │    │
│  │ - Schemas            │         │ - Correlation detection   │    │
│  │ - Connection pooling │         │ - Missing value analysis  │    │
│  └──────────────────────┘         │ - Distribution analysis   │    │
│                                   │ - HTML/JSON generation    │    │
│  ┌──────────────────────┐         └───────────────────────────┘    │
│  │ OpenAI API           │                                           │
│  │ - GPT-4o-mini        │                                           │
│  │ - Chat completions   │                                           │
│  │ - Structured outputs │                                           │
│  └──────────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          OUTPUT LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐    │
│  │ HTML Reports   │  │ JSON Profiles  │  │ Workflow Results   │    │
│  │ - Final report │  │ - Statistics   │  │ - Complete JSON    │    │
│  │ - Visual       │  │ - Metrics      │  │ - All phases       │    │
│  │ - Formatted    │  │ - Correlations │  │ - Timestamped      │    │
│  └────────────────┘  └────────────────┘  └────────────────────┘    │
│                                                                     │
│  Saved to: ge_reports/ directory                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Workflow Sequence

### Phase 1: Planning
```
User Goal → PlannerAgent
                │
                ▼
         Loads schema.json
                │
                ▼
         Creates plan with:
         - Query tasks for DataAgent
         - Profiling tasks for DataProfilingAgent  
         - Execution sequence
         - Success criteria
                │
                ▼
         Returns: DataQualityPlan
```

### Phase 2: Investigation
```
DataQualityPlan → [DataAgent + DataProfilingAgent]
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
      DataAgent                   DataProfilingAgent
           │                               │
    Execute SQL queries             Profile datasets
    Gather evidence                 Generate reports
    Analyze samples                 Extract statistics
           │                               │
           ▼                               ▼
    DataAgentReport              DataProfilingReport
           │                               │
           └───────────────┬───────────────┘
                           ▼
                  Combined Results
```

### Phase 3: Analysis
```
Combined Results → SummarizerAgent
                          │
                          ▼
                  Correlate findings
                  Read profiling JSON
                  Identify issues
                  Assign severity
                  Create recommendations
                          │
                          ▼
                DataQualityAgentReport
```

### Phase 4: Reporting
```
All Results → ReportAgent
                  │
                  ▼
          Format as HTML
          Add sections:
          - Executive Summary
          - Data Profile
          - Quality Assessment
          - Issues & Severity
          - Recommendations
          - Visualizations
                  │
                  ▼
            HTML Report
                  │
                  ▼
         Saved to ge_reports/
```

## Data Flow Example

```
User: "Analyze missing values in RIDEBOOKING table"
  │
  ▼
PlannerAgent creates plan:
  • Query Task 1: "Check for null values in critical columns"
  • Query Task 2: "Analyze missing patterns by date"
  • Profiling Task 1: "Profile RIDEBOOKING to get distributions"
  │
  ▼
DataAgent executes:
  • SELECT COUNT(*) FROM RIDEBOOKING WHERE BOOKING_VALUE IS NULL
  • SELECT DATE, COUNT(*) WHERE ... IS NULL GROUP BY DATE
  │
DataProfilingAgent executes:
  • SELECT * FROM RIDEBOOKING LIMIT 100000
  • Creates ProfileReport
  • Generates HTML + JSON reports
  │
  ▼
SummarizerAgent analyzes:
  • Correlates query results with profiling stats
  • Identifies: "15% missing BOOKING_VALUE (Critical)"
  • Recommends: "Impute using median per vehicle type"
  │
  ▼
ReportAgent formats:
  • Professional HTML with all findings
  • Links to profiling reports
  • Visualizations and tables
  │
  ▼
Output:
  • ge_reports/data_quality_report_*.html
  • ge_reports/*_profile_*.html
  • ge_reports/*_profile_*.json
  • ge_reports/workflow_results_*.json
```

## Component Details

### Pydantic Models (Structured Outputs)

All agents use Pydantic models for structured communication:

```python
# Planning
DataQualityPlan:
  - goal: str
  - query_tasks: list[QueryTask]
  - profiling_tasks: list[ProfilingTask]
  - execution_sequence: list[str]
  - success_criteria: list[str]

# Investigation
DataAgentReport:
  - plan_goal: str
  - tasks_executed: list[QueryExecution]
  - next_steps: list[str]

DataProfilingReport:
  - plan_goal: str
  - tasks_executed: list[DataProfilingTasksExecuted]
  - next_steps: list[str]

# Analysis
DataQualityAgentReport:
  - summary: str
  - issues: list[DataQualityIssue]
  - recommendations: list[str]
  - required_followup_queries: list[str]
  - analysis_complete: bool

# Reporting
ReportResponse:
  - html: str
  - thoughts: str
```

### Agent Communication

Agents communicate via AutoGen's **RoundRobinGroupChat** with:
- Structured message types
- Custom termination conditions
- Message history tracking
- Streaming support (optional)

### Tool Architecture

```
Agent → ToolFactory → Tool → External Service
                              │
                              ├─ SnowflakeQueryEngine → Snowflake DB
                              ├─ ydata-profiling → Statistical analysis
                              └─ File system → Read/write reports
```

## File Structure

```
DataSentinel/
├── agent/
│   ├── __init__.py
│   ├── Orchestrator.py              # Multi-phase workflow coordinator
│   ├── PlannerAgent.py              # Creates execution plans
│   ├── DataAgent.py                 # SQL investigation agent
│   ├── DataProfilingAgent.py        # Statistical profiling agent
│   ├── SummarizerAgent.py           # Analysis & synthesis agent
│   ├── ReportAgent.py               # HTML report generation agent
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   └── ModelFactory.py          # OpenAI client factory
│   │
│   └── tool/
│       ├── __init__.py
│       ├── SnowflakeQueryEngine.py              # Query execution
│       ├── SnowflakeQueryToolFactory.py         # Query tool factory
│       ├── SnowflakeDataProfilingTool.py        # Profiling implementation
│       ├── SnowflakeDataProfilingToolFactory.py # Profiling tool factory
│       ├── ProfilingReportReaderTool.py         # JSON report parser
│       └── ProfilingReportReaderToolFactory.py  # Reader tool factory
│
├── tests/
│   └── agent/
│       ├── PlannerAgent_test.py
│       ├── DataAgent_test.py
│       ├── DataProfilingAgent_test.py
│       ├── SummarizerAgent_test.py
│       └── ReportAgent_test.py
│
├── metadata/
│   └── schema.json                  # Database schema definition
│
├── ge_reports/                      # Generated reports directory
│   ├── *_profile_*.html            # ydata-profiling HTML reports
│   ├── *_profile_*.json            # ydata-profiling JSON data
│   ├── data_quality_report_*.html  # Final reports from ReportAgent
│   └── workflow_results_*.json     # Complete workflow outputs
│
├── app.py                          # Main application entry
├── orchestrator_example.py         # Usage examples
├── requirements.txt                # Dependencies
├── setup.py                        # Package setup
├── ARCHITECTURE.md                 # This file
├── README_Orchestrator.md          # Orchestrator documentation
└── QUICKREF_Orchestrator.md        # Quick reference guide
```

## Technology Stack

### Core Technologies
- **Python 3.11+**: Programming language
- **AutoGen 0.7+**: Multi-agent framework
  - `autogen-core`: Core agent functionality
  - `autogen-agentchat`: Chat-based agents
  - `autogen-ext[openai]`: OpenAI integration
- **ydata-profiling**: Statistical data profiling
- **Snowflake**: Cloud data warehouse
- **Pandas**: Data manipulation
- **OpenAI GPT-4o-mini**: Language model

### Key Libraries
```
autogen-core>=0.7.0
autogen-agentchat>=0.7.0
autogen-ext[openai]>=0.7.0
snowflake-connector-python>=3.12.0
ydata-profiling>=4.0.0
sqlalchemy>=2.0.0
pandas>=2.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
matplotlib>=3.7.0
```

### Important Configuration

**Matplotlib Backend** (in `SnowflakeDataProfilingTool.py`):
```python
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for thread safety on macOS
```

This prevents the "NSWindow should only be instantiated on the main thread" error when running agents in threads.

## Environment Configuration

Required environment variables (`.env` file):

```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=YOUR_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=SYSADMIN

# OpenAI API
OPENAI_API_KEY=your_openai_api_key
```

## Security Considerations

### Credentials Management
- All credentials stored in environment variables
- Never hardcoded in source code
- `.env` file excluded from version control
- Support for `.gitignore` patterns

### Connection Security
- Encrypted Snowflake connections
- Token-based authentication support
- Role-based access control (RBAC)
- Connection pooling with automatic cleanup

### Data Privacy
- No PII exposure in logs or reports
- Configurable data sampling limits
- Query result size constraints
- Secure report storage

## Scalability & Performance

### Horizontal Scaling
- Independent agent instances
- Parallel task execution (planned)
- Distributed report generation

### Vertical Scaling
- Adjustable Snowflake warehouse sizes
- Configurable memory limits
- Row sampling strategies (100k row limit for profiling)

### Performance Optimization
- Query result caching in SnowflakeQueryEngine
- Incremental profiling support
- Selective column analysis
- Minimal mode for faster profiling

### Resource Management
- Connection pooling
- Automatic connection cleanup
- Memory-efficient DataFrame operations
- Streaming support for large result sets

## Error Handling & Resilience

### Agent-Level
- Try-catch blocks in all agent operations
- Structured error reporting
- Graceful degradation (phases can fail independently)

### Tool-Level
- Connection retry logic
- Query timeout handling
- Invalid data handling (e.g., TRY_CAST in SQL)

### Orchestrator-Level
- Phase-by-phase error tracking
- Comprehensive error logging
- Traceback capture
- Partial result preservation

## Monitoring & Observability

### Logging
- Phase-by-phase progress indicators
- Emoji-based status indicators (🔧, ✅, ❌, ⚠️, 📋, 🔍, 📊, 📄)
- Detailed operation logs

### Output Tracking
- All reports timestamped
- Workflow results saved as JSON
- Complete message history preserved
- Links between related reports

### Metrics
- Query execution times
- Row counts processed
- Number of issues identified
- Agent interaction counts

## Design Principles

1. **Modularity**: Each agent has a single, well-defined responsibility
2. **Composability**: Agents can be combined in different workflows
3. **Extensibility**: Easy to add new agents or tools
4. **Type Safety**: Pydantic models ensure data contract integrity
5. **Transparency**: All decisions and findings are traceable
6. **Resilience**: Failures in one phase don't crash the entire workflow
7. **Testability**: Each component can be tested independently

## Future Enhancements

### Planned Features
- [ ] Real-time data quality monitoring
- [ ] Automated remediation suggestions
- [ ] Integration with data lineage tools
- [ ] Support for additional databases (PostgreSQL, MySQL)
- [ ] Custom expectation creation
- [ ] Dashboard for historical trends
- [ ] Slack/Teams notifications
- [ ] API endpoint for programmatic access
- [ ] Parallel agent execution
- [ ] Incremental profiling for large tables

### Architecture Evolution
- [ ] Plugin system for custom agents
- [ ] Distributed agent execution
- [ ] Cloud-native deployment options
- [ ] Real-time collaboration features
- [ ] Advanced caching strategies

## References

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/)
- [Snowflake Python Connector](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Last Updated**: October 14, 2025  
**Version**: 2.0  
**Architecture Status**: Production-Ready
