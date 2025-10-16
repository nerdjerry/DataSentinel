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
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ PHASE 2: INVESTIGATION                                      │   │
│  │ ┌────────────────────┐      ┌──────────────────────────┐    │   │
│  │ │ DataAgent          │      │ DataProfilingAgent       │    │   │
│  │ │ - SQL queries      │      │ - ydata-profiling        │    │   │
│  │ │ - Evidence         │      │ - Statistical analysis   │    │   │
│  │ │   gathering        │      │ - HTML/JSON reports      │    │   │
│  │ │ - Tools:           │      │ - Tools:                 │    │   │
│  │ │   • query_tool     │      │   • profile_tool         │    │   │
│  │ │   • table_info     │      │   • (uses query_engine)  │    │   │
│  │ │   • list_tables    │      │                          │    │   │
│  │ │ - Output:          │      │ - Output:                │    │   │
│  │ │   DataAgentReport  │      │   DataProfilingReport    │    │   │
│  │ └────────────────────┘      └──────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
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
│                                                                    │
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
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          MODEL LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ ModelFactory                                                  │  │
│  │ - Creates OpenAI client instances                             │  │
│  │ - Model: gpt-5-mini (default)                                 │  │
│  │ - API key management via environment variables                │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       TOOL FACTORY LAYER                            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌────────────────────────────────┐   │
│  │ SnowflakeQuery           │  │ SnowflakeDataProfiling         │   │
│  │ ToolFactory              │  │ ToolFactory                    │   │
│  │                          │  │                                │   │
│  │ - create_query_tool()    │  │ - create_profile_tool()        │   │
│  │ - create_table_info()    │  │                                │   │
│  │ - create_list_tables()   │  │                                │   │
│  └──────────┬───────────────┘  └────────────┬───────────────────┘   │
│             │                               │                       │
│  ┌──────────┴───────────────┐  ┌────────────┴───────────────────┐   │
│  │ ProfilingReportReader    │  │                                │   │
│  │ ToolFactory              │  │                                │   │
│  │                          │  │                                │   │
│  │ - create_read_tool()     │  │                                │   │
│  └──────────────────────────┘  └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                           TOOL LAYER                                │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ SnowflakeQueryEngine                                        │    │
│  │ - execute_query() → DataFrame/JSON/Dict                     │    │
│  │ - get_table_info() → Schema information                     │    │
│  │ - list_tables() → Available tables                          │    │
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
│  │ Snowflake DataWH     │         │ ydata-profiling           │    │
│  │ - RIDEBOOKING table  │         │ - ProfileReport           │    │
│  │ - Tables/Views       │         │ - Statistical analysis    │    │
│  │ - Schemas            │         │ - Correlation detection   │    │
│  │ - Connection pooling │         │ - Missing value analysis  │    │
│  └──────────────────────┘         │ - Distribution analysis   │    │
│                                   │ - HTML/JSON generation    │    │
│  ┌──────────────────────┐         └───────────────────────────┘    │
│  │ OpenAI API           │                                           │
│  │ - GPT-5-mini         │                                           │
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

### Phase 2: Investigation (Parallel Execution)
```
DataQualityPlan → [DataAgent + DataProfilingAgent]
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
    [Multiple Query Tasks]       [Multiple Profiling Tasks]
    (Executed Concurrently)      (Executed Concurrently)
           │                               │
    Each task runs in                Each task runs in
    separate async task             separate async task
           │                               │
           ▼                               ▼
    List[DataAgentReport]        List[DataProfilingReport]
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
  • Query Task 3: "Identify negative or zero booking values"
  • Profiling Task 1: "Profile RIDEBOOKING to get distributions"
  │
  ▼
DataAgent executes (3 tasks concurrently via asyncio.gather):
  Task 1: SELECT COUNT(*) FROM RIDEBOOKING WHERE BOOKING_VALUE IS NULL
  Task 2: SELECT DATE, COUNT(*) WHERE ... IS NULL GROUP BY DATE
  Task 3: SELECT * FROM RIDEBOOKING WHERE BOOKING_VALUE <= 0
  │
DataProfilingAgent executes (concurrently):
  Task 1: SELECT * FROM RIDEBOOKING LIMIT 100000
         Creates ProfileReport
         Generates HTML + JSON reports
  │
  ▼
Results aggregated:
  • List[DataAgentReport] with 3 query results
  • List[DataProfilingReport] with 1 profiling result
  │
  ▼
SummarizerAgent analyzes:
  • Reads profiling JSON using ProfilingReportReaderTool
  • Correlates all query results with profiling stats
  • Identifies: "15% missing BOOKING_VALUE (Critical)"
  • Recommends: "Impute using median per vehicle type"
  │
  ▼
ReportAgent formats:
  • Professional HTML with all findings
  • Tab navigation linking to profiling reports
  • Visualizations and tables
  • Relative links to detailed profiling HTML
  │
  ▼
Output:
  • ge_reports/data_quality_report_*.html (main report)
  • ge_reports/*_profile_*.html (profiling report)
  • ge_reports/*_profile_*.json (profiling data)
  • ge_reports/workflow_results_*.json (complete workflow)
```

## Component Details

### Pydantic Models (Structured Outputs)

All agents use Pydantic models for structured communication:

```python
# Planning (PlannerAgent.py)
QueryTask:
  - goal: str  # What DataAgent should investigate

ProfilingTask:
  - goal: str  # What to profile

DataQualityPlan:
  - goal: str
  - query_tasks: list[QueryTask]
  - profiling_tasks: list[ProfilingTask]
  - execution_sequence: list[str]
  - success_criteria: list[str]

# Investigation (DataAgent.py)
QueryExecution:
  - investigation_goal: str
  - sql_query: str
  - row_count: int
  - sample_data: str
  - summary: str

DataAgentReport:
  - plan_goal: str
  - tasks_executed: list[QueryExecution]
  - next_steps: list[str]

# Profiling (DataProfilingAgent.py)
DataProfilingTasksExecuted:
  - task_purpose: str
  - query_or_dataset: str
  - row_count: int
  - column_count: int
  - html_report_path: str
  - json_report_path: str

DataProfilingReport:
  - plan_goal: str
  - tasks_executed: list[DataProfilingTasksExecuted]
  - next_steps: list[str]

# Analysis (SummarizerAgent.py)
DataQualityIssue:
  - type: str
  - severity: str  # "Critical", "High", "Medium", "Low"
  - evidence_query: str
  - evidence_description: str

DataQualityAgentReport:
  - summary: str
  - issues: list[DataQualityIssue]
  - recommendations: list[str]
  - required_followup_queries: list[str]
  - analysis_complete: bool

# Reporting (ReportAgent.py)
ReportResponse:
  - html: str
  - thoughts: str
```

### Agent Communication

### Orchestrator Architecture

The `Orchestrator` class coordinates the entire workflow with the following features:

**Agent Communication**:
- Uses AutoGen's **RoundRobinGroupChat** for single-agent teams per phase
- **Structured message types**: Using `StructuredMessage[DataQualityPlan]`, `StructuredMessage[DataAgentReport]`, etc.
- **Custom termination conditions**: `MaxMessageTermination` with configurable max_messages per phase
- Message history tracking
- Streaming support (optional, disabled for structured outputs)
- **Pydantic-based structured outputs**: All agents return typed Pydantic models instead of plain text
- **Reflection disabled**: `reflect_on_tool_use=False` to prevent JSON parsing issues with structured outputs

**Concurrent Execution** (Phase 2 - Investigation):
```python
# Execute all query tasks concurrently
query_coroutines = [execute_query_task(task) for task in plan.query_tasks]
query_results = await asyncio.gather(*query_coroutines, return_exceptions=True)

# Execute all profiling tasks concurrently
profiling_coroutines = [execute_profiling_task(task) for task in plan.profiling_tasks]
profiling_results = await asyncio.gather(*profiling_coroutines, return_exceptions=True)
```

**Key Methods**:
- `run_analysis(goal)`: Main entry point for complete workflow
- `_run_planning_phase(goal)`: Phase 1 - Create execution plan
- `_run_investigation_phase(plan)`: Phase 2 - Execute tasks concurrently
- `_run_analysis_phase(...)`: Phase 3 - Synthesize findings
- `_run_reporting_phase(...)`: Phase 4 - Generate HTML report
- `_save_results(results)`: Save complete workflow results to JSON

### Tool Architecture

```
### Model Configuration

**ModelFactory** (`agent/model/ModelFactory.py`):
- Creates `OpenAIChatCompletionClient` instances
- Default model: `gpt-5-mini` (OpenAI GPT-4o-mini alias)
- API key loaded from environment variable `OPENAI_API_KEY`
- Uses `python-dotenv` for environment configuration
- No temperature configuration (uses model defaults)

```python
@staticmethod
def get_model(model: str = "gpt-5-mini"):
    return OpenAIChatCompletionClient(
        model=model,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
```

### Tool Architecture

```
Agent → ToolFactory → Tool → External Service
                              │
                              ├─ SnowflakeQueryEngine → Snowflake DB
                              ├─ ydata-profiling → Statistical analysis
                              └─ File system → Read/write reports
```
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
├── WorkflowRunner.py               # Workflow execution runner
├── requirements.txt                # Dependencies
├── setup.py                        # Package setup
├── run_tests.sh                    # Test execution script
└── ARCHITECTURE.md                 # This file
```

## Technology Stack

### Core Technologies
- **Python 3.11+**: Programming language
- **AutoGen 0.7.5**: Multi-agent framework
  - `autogen-core==0.7.5`: Core agent functionality
  - `autogen-agentchat==0.7.5`: Chat-based agents
  - `autogen-ext[openai]==0.7.5`: OpenAI integration
- **ydata-profiling 4.17.0**: Statistical data profiling
- **Snowflake**: Cloud data warehouse
  - `snowflake-connector-python==3.18.0`: Python connector
  - `snowflake-sqlalchemy==1.7.7`: SQLAlchemy integration
- **Pandas 2.3.3**: Data manipulation
- **OpenAI GPT-4o-mini**: Language model (accessed via gpt-5-mini alias)

### Key Libraries
```
# AutoGen Framework - Multi-agent orchestration
autogen-core==0.7.5
autogen-agentchat==0.7.5
autogen-ext[openai]==0.7.5

# Snowflake Database Integration
snowflake-connector-python==3.18.0
snowflake-sqlalchemy==1.7.7

# Data Analysis and Profiling
pandas==2.3.3
ydata-profiling==4.17.0

# Environment Configuration
python-dotenv==1.1.1
```

### Important Configuration

**Matplotlib Backend** (in `SnowflakeDataProfilingTool.py`):
```python
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for thread safety on macOS
```

This prevents the "NSWindow should only be instantiated on the main thread" error when running profiling agents with async/concurrent execution.

**Agent System Messages**:
All agents use JSON-formatted system messages with:
- Clear role definitions
- Structured output format specifications
- Query best practices (DataAgent includes SQL error handling guidelines)
- Database schema information
- Termination conditions
- Constraints and security guidelines

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
- **Parallel task execution (implemented)**: Multiple query tasks and profiling tasks execute concurrently using asyncio.gather()
- Distributed report generation
- Each task runs in its own async coroutine for concurrent execution

### Vertical Scaling
- Adjustable Snowflake warehouse sizes
- Configurable memory limits
- Row sampling strategies (100k row limit for profiling)

### Performance Optimization
- Query result caching in SnowflakeQueryEngine
- Incremental profiling support
- Selective column analysis
- Minimal mode for faster profiling
- Concurrent execution of multiple investigation and profiling tasks
- Exception handling per task to prevent cascade failures

### Resource Management
- Connection pooling
- Automatic connection cleanup
- Memory-efficient DataFrame operations
- Streaming support for large result sets
- Thread-safe matplotlib backend (Agg) for concurrent profiling

## Error Handling & Resilience

### Agent-Level
- Try-catch blocks in all agent operations
- Structured error reporting via Pydantic models
- Graceful degradation (phases can fail independently)
- `reflect_on_tool_use=False` to prevent JSON parsing issues

### Tool-Level
- Connection retry logic
- Query timeout handling
- Invalid data handling (e.g., TRY_CAST for numeric conversions only)
- Special handling for DATE/TIME columns (use CAST/TO_VARCHAR instead of TRY_CAST)

### Orchestrator-Level
- Phase-by-phase error tracking
- Comprehensive error logging with emoji indicators (🔧, ✅, ❌, ⚠️)
- Traceback capture in workflow results
- Partial result preservation
- **Per-task exception handling**: `asyncio.gather(..., return_exceptions=True)` prevents one task failure from crashing all concurrent tasks
- Error filtering: Individual task failures logged but don't stop workflow

### Concurrent Execution Error Handling
```python
# Execute tasks concurrently with exception handling
results = await asyncio.gather(*coroutines, return_exceptions=True)

# Filter out exceptions
for result in results:
    if isinstance(result, Exception):
        print(f"Task failed with error: {str(result)}")
    elif result is not None:
        all_results.append(result)
```

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

## Recent Enhancements (v2.1)

### Completed Features
- [x] **Parallel agent execution**: Multiple query and profiling tasks execute concurrently using asyncio.gather()
- [x] **Structured outputs**: All agents return typed Pydantic models for type safety
- [x] **Concurrent task processing**: Each query/profiling task runs in separate async coroutine
- [x] **Exception handling per task**: Failures in individual tasks don't crash the entire workflow
- [x] **Multi-task reporting**: Support for multiple DataAgentReports and DataProfilingReports in analysis phase

### Architecture Evolution
- [ ] Plugin system for custom agents
- [ ] Distributed agent execution across multiple nodes
- [ ] Cloud-native deployment options (Kubernetes, Docker)
- [ ] Real-time collaboration features
- [ ] Advanced caching strategies
- [ ] Agent performance monitoring and metrics

## References

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/)
- [Snowflake Python Connector](https://docs.snowflake.com/en/user-guide/python-connector.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Last Updated**: October 16, 2025  
**Version**: 2.1  
**Architecture Status**: Production-Ready
