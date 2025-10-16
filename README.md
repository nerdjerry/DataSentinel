# 🛡️ DataSentinel

A multi-agent orchestration platform for comprehensive data quality analysis using AutoGen and Snowflake.

## 🌟 Overview

DataSentinel uses a sophisticated multi-agent system to perform deep data quality analysis on Snowflake databases. It coordinates specialized AI agents through four distinct phases to investigate, profile, analyze, and report on data quality issues.

## 🚀 Quick Start

### Using Streamlit Web Interface (Recommended)

The easiest way to use DataSentinel is through the Streamlit web interface:

**macOS/Linux:**
```bash
./run_streamlit.sh
```
**Or manually:**
```bash
streamlit run streamlit_app.py
```

The web interface will open at `http://localhost:8501` where you can:
- Enter data quality goals interactively
- Monitor the 4-phase workflow in real-time
- View execution logs and metrics
- Download generated reports

## 📋 Features

### Multi-Agent Architecture
- **PlannerAgent**: Creates comprehensive execution plans
- **DataAgent**: Executes SQL queries to gather evidence
- **DataProfilingAgent**: Generates statistical profiles using ydata-profiling
- **SummarizerAgent**: Synthesizes findings and identifies issues
- **ReportAgent**: Creates professional HTML reports

### 4-Phase Workflow
1. **Planning** 📋: Break down goals into query and profiling tasks
2. **Investigation** 🔍: Execute tasks concurrently for fast results
3. **Analysis** 📊: Correlate findings and identify data quality issues
4. **Reporting** 📄: Generate comprehensive HTML reports

### Key Capabilities
- ✅ Concurrent task execution for optimal performance
- ✅ Structured Pydantic outputs for type safety
- ✅ Real-time progress monitoring (Streamlit)
- ✅ Professional HTML report generation
- ✅ Statistical profiling with ydata-profiling
- ✅ Snowflake integration with connection pooling
- ✅ Comprehensive error handling and logging

## 🔧 Installation

### Prerequisites
- Python 3.11 or higher
- Snowflake account with access credentials
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DataSentinel
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
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

## 📦 Dependencies

```
# AutoGen Framework
autogen-core==0.7.5
autogen-agentchat==0.7.5
autogen-ext[openai]==0.7.5

# Snowflake Integration
snowflake-connector-python==3.18.0
snowflake-sqlalchemy==1.7.7

# Data Analysis
pandas==2.3.3
ydata-profiling==4.17.0

# Web Interface
streamlit==1.39.0

# Configuration
python-dotenv==1.1.1
```

## 🎯 Usage Examples

### Example 1: Missing Values Analysis

**Streamlit UI:**
1. Open the app: `./run_streamlit.sh`
2. Enter goal: "Analyze missing values in the RIDEBOOKING table"
3. Click "Run Analysis"
4. Watch the progress through each phase


### Example 2: Data Distribution Analysis

```python
goal = "Check data distribution and identify outliers in booking amounts"
results = await orchestrator.run_analysis(goal)
```

### Example 3: Completeness Check

```python
goal = "Verify data completeness across all critical columns"
results = await orchestrator.run_analysis(goal)
```

## 📊 Workflow Phases

### Phase 1: Planning 📋
```
User Goal → PlannerAgent
  ↓
Loads schema.json
  ↓
Creates plan:
  - Query tasks for DataAgent
  - Profiling tasks for DataProfilingAgent
  - Execution sequence
  - Success criteria
```

### Phase 2: Investigation 🔍
```
Plan → [DataAgent + DataProfilingAgent]
  ↓
Concurrent execution:
  - Multiple query tasks (async)
  - Multiple profiling tasks (async)
  ↓
Results aggregated
```

### Phase 3: Analysis 📊
```
Combined Results → SummarizerAgent
  ↓
Correlates findings
Identifies issues
Assigns severity
Creates recommendations
```

### Phase 4: Reporting 📄
```
All Results → ReportAgent
  ↓
Generates HTML report with:
  - Executive summary
  - Data profiles
  - Quality assessment
  - Issues & severity
  - Recommendations
  - Visualizations
```

## 📁 Project Structure

```
DataSentinel/
├── agent/                          # Agent implementations
│   ├── Orchestrator.py            # Workflow coordinator
│   ├── PlannerAgent.py            # Planning agent
│   ├── DataAgent.py               # Query execution agent
│   ├── DataProfilingAgent.py      # Profiling agent
│   ├── SummarizerAgent.py         # Analysis agent
│   ├── ReportAgent.py             # Report generation agent
│   ├── model/                     # Model factory
│   └── tool/                      # Tools and engines
├── tests/                         # Unit tests
├── metadata/                      # Schema definitions
├── ge_reports/                    # Generated reports
├── streamlit_app.py               # Web interface
├── WorkflowRunner.py              # CLI runner
├── run_streamlit.sh               # Streamlit launcher (Unix)
├── run_streamlit.bat              # Streamlit launcher (Windows)
├── requirements.txt               # Dependencies
├── ARCHITECTURE.md                # Architecture documentation
├── STREAMLIT_README.md            # Streamlit guide
└── README.md                      # This file
```

## 🧪 Testing

Run all tests:
```bash
./run_tests.sh
```

Run specific tests:
```bash
python -m pytest tests/agent/PlannerAgent_test.py
python -m pytest tests/agent/DataAgent_test.py
python -m pytest tests/agent/ReportAgent_test.py
```

## 📈 Output

DataSentinel generates several types of output:

### HTML Reports
- **Main Report**: `ge_reports/data_quality_report_*.html`
  - Executive summary
  - Detailed findings
  - Visualizations
  - Recommendations

### Profiling Reports
- **HTML Profile**: `ge_reports/*_profile_*.html`
  - Statistical analysis
  - Distribution charts
  - Correlation matrices
  - Missing value analysis

- **JSON Profile**: `ge_reports/*_profile_*.json`
  - Raw profiling data
  - Metrics and statistics

### Workflow Results
- **Results JSON**: `ge_reports/workflow_results_*.json`
  - Complete workflow output
  - All phase results
  - Timestamps

## 🔒 Security

- ✅ All credentials stored in environment variables
- ✅ No hardcoded secrets
- ✅ Encrypted Snowflake connections
- ✅ Role-based access control (RBAC)
- ✅ Secure report storage

**Important:** Never commit `.env` files to version control!

## ⚡ Performance

- **Concurrent Execution**: Query and profiling tasks run in parallel using asyncio
- **Connection Pooling**: Efficient Snowflake connection management
- **Smart Sampling**: 100k row limit for profiling to balance speed and accuracy
- **Caching**: Query result caching in SnowflakeQueryEngine
- **Error Isolation**: Individual task failures don't crash the workflow

## 🐛 Troubleshooting

### Common Issues

**Import Error:**
```
ModuleNotFoundError: No module named 'agent'
```
**Solution:** Run from project root directory

**Connection Error:**
```
Snowflake connection failed
```
**Solution:** Check `.env` file credentials and network connectivity

**Streamlit Not Found:**
```
streamlit: command not found
```
**Solution:** Install Streamlit: `pip install streamlit`

## 📖 Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed system architecture
- **[AutoGen Documentation](https://microsoft.github.io/autogen/)**: AutoGen framework
- **[ydata-profiling Docs](https://docs.profiling.ydata.ai/)**: Profiling library

## 🛠️ Technology Stack

- **Python 3.11+**: Programming language
- **AutoGen 0.7.5**: Multi-agent framework
- **OpenAI GPT-4o-mini**: Language model (via gpt-5-mini)
- **Streamlit 1.39.0**: Web interface
- **ydata-profiling 4.17.0**: Statistical profiling
- **Snowflake**: Cloud data warehouse
- **Pandas 2.3.3**: Data manipulation

## 🚧 Roadmap

- [ ] Support for additional databases (PostgreSQL, MySQL, BigQuery)
- [ ] Custom agent plugins
- [ ] Real-time monitoring dashboard
- [ ] Scheduled workflow execution
- [ ] Multi-user collaboration features
- [ ] Advanced caching strategies
- [ ] Distributed agent execution

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

[Your License Here]

## 👥 Authors

[Prateek Singhal]

## 🙏 Acknowledgments

- AutoGen team for the multi-agent framework
- ydata-profiling for statistical profiling capabilities
- Streamlit for the amazing web framework

---

**Version**: 2.1  
**Last Updated**: October 16, 2025  
**Status**: Production-Ready

**Happy Data Quality Analysis! 🛡️**
