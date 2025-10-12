# ydata-profiling Integration

## Overview

The `SnowflakeDataProfilingTool` now uses **ydata-profiling** (formerly pandas-profiling) for comprehensive data profiling. This provides significantly more powerful analysis capabilities compared to basic pandas statistics or manual profiling.

## Why ydata-profiling?

### Key Benefits

1. **Comprehensive Statistics**
   - Descriptive statistics for all variables
   - Correlations (Pearson, Spearman, Kendall, Cramér's V, φk)
   - Missing values analysis
   - Duplicate rows detection
   - Variable type inference

2. **Interactive HTML Reports**
   - Beautiful, professional-looking reports
   - Interactive visualizations and charts
   - Histograms, distribution plots
   - Correlation matrices with heatmaps
   - Sample data preview

3. **Deep Analysis**
   - Identifies highly correlated variables
   - Detects constant and unique variables
   - Highlights potential data quality issues
   - Provides warnings and alerts
   - Analyzes text patterns and lengths

4. **Zero Configuration**
   - Works out of the box
   - Automatic type detection
   - Intelligent metric selection based on data types
   - Minimal setup required

## Features Available

### Dataset Overview
- Number of variables and observations
- Missing cells count and percentage
- Duplicate rows detection
- Variable types distribution
- Dataset size and memory usage

### Variable Analysis
Each variable gets detailed analysis including:
- **Numerical**: min, max, mean, median, mode, std, variance, range, IQR, CV, skewness, kurtosis
- **Categorical**: unique values, most frequent values, category distribution
- **Text**: length statistics, character distribution, unicode categories
- **Date/Time**: min, max, range, temporal patterns

### Correlations
- **Pearson**: For numerical variables
- **Spearman**: For ranked variables
- **φk (Phik)**: For categorical-numerical correlations
- **Cramér's V**: For categorical-categorical correlations

### Visualizations
- Distribution histograms
- Missing value heatmaps
- Correlation matrices
- Value frequency charts
- Interactions between variables

### Data Quality Warnings
Automatic alerts for:
- High cardinality variables
- Variables with high percentage of missing values
- Constant variables (single value)
- Variables with high correlation
- Highly skewed distributions
- Imbalanced categorical variables

## Usage

### Basic Profiling

```python
from agent.tool.SnowflakeDataProfilingTool import SnowflakeDataProfilingTool

tool = SnowflakeDataProfilingTool(reports_dir="ge_reports")

result = tool.profile_data(
    query="SELECT * FROM RIDEBOOKING LIMIT 1000",
    table_name="ridebooking_analysis",
    goal="Profile ride booking data for quality assessment",
    generate_html=True,
    generate_json=True
)

if result['success']:
    print(f"HTML Report: {result['report_paths']['html']}")
    print(f"JSON Report: {result['report_paths']['json']}")
    print(f"Missing Cells: {result['summary']['missing_cells_pct']:.2f}%")
    print(f"Duplicate Rows: {result['summary']['duplicate_rows']}")
```

### Minimal Mode (Faster)

For large datasets, use minimal mode for faster profiling:

```python
result = tool.profile_data(
    query="SELECT * FROM LARGE_TABLE LIMIT 10000",
    table_name="large_dataset",
    minimal_mode=True  # Faster, less detailed
)
```

### AutoGen Integration

The tool is designed to work with AutoGen agents:

```python
from agent.tool.SnowflakeDataProfilingToolFactory import SnowflakeDataProfilingToolFactory

# Create tools for AutoGen agents
factory = SnowflakeDataProfilingToolFactory()
profile_tool = factory.create_profile_tool()

# Use with DataProfilingAgent
from agent.DataProfilingAgent import create_data_profiling_agent

agent = create_data_profiling_agent(
    name="DataProfiler",
    tools=[profile_tool]
)
```

## Report Structure

### HTML Report Sections

1. **Overview**
   - Dataset statistics
   - Variable types
   - Warnings and alerts

2. **Variables**
   - Detailed statistics per variable
   - Distribution visualizations
   - Value frequencies

3. **Correlations**
   - Correlation matrices
   - Highly correlated pairs
   - Interactive heatmaps

4. **Missing Values**
   - Missing value patterns
   - Heatmap visualization
   - Dendrogram of nullity correlation

5. **Sample**
   - First/last rows
   - Random sample preview

### JSON Report

The JSON report contains the complete statistical description in a structured format, suitable for:
- Programmatic analysis
- Integration with other systems
- Automated quality checks
- Data pipeline validation

## Performance Considerations

### Dataset Size Recommendations

- **Small datasets** (< 10,000 rows): Use full profiling mode
- **Medium datasets** (10,000 - 100,000 rows): Use full profiling, expect 10-30 seconds
- **Large datasets** (> 100,000 rows): Use minimal mode or sample data

### Sampling Strategy

For very large tables:

```python
# Profile a representative sample
query = """
SELECT * 
FROM LARGE_TABLE 
TABLESAMPLE (10000 ROWS)  -- Sample 10K rows
"""
```

## Dependencies

The following packages are installed as part of ydata-profiling:

```
ydata-profiling>=4.0.0
pandas>=1.5.0
numpy>=1.16.0
scipy>=1.4.1
matplotlib>=3.5.0
seaborn>=0.10.1
```

## Comparison with Previous Approach

| Feature | Manual Pandas | Great Expectations | ydata-profiling |
|---------|---------------|-------------------|-----------------|
| Setup complexity | Low | High | Low |
| Report quality | Basic | Good | Excellent |
| Visualizations | Manual | Limited | Comprehensive |
| Correlations | Manual | No | Automatic |
| Missing values | Basic stats | Validation only | Deep analysis |
| Ease of use | Medium | Complex | Very Easy |
| Report format | Custom HTML | Custom/Data Docs | Professional HTML |
| JSON export | Custom | Yes | Yes |
| Performance | Fast | Medium | Medium |

## Best Practices

1. **Use Sampling for Large Datasets**
   - Profile samples rather than entire tables
   - Use Snowflake's TABLESAMPLE for representative samples

2. **Enable Minimal Mode for Speed**
   - Use `minimal_mode=True` for quick assessments
   - Switch to full mode for detailed analysis

3. **Review Warnings**
   - Pay attention to data quality warnings in reports
   - Address high cardinality and missing value issues

4. **Archive Reports**
   - Keep historical reports for tracking data quality over time
   - Compare reports to detect data drift

5. **Integrate with CI/CD**
   - Run profiling as part of data pipeline validation
   - Use JSON reports for automated quality gates

## Example Output

The tool generates rich, interactive HTML reports that include:

- 📊 **Dataset Overview**: 100 rows, 21 variables
- 🔢 **Numerical Analysis**: Statistics, distributions, outliers
- 📝 **Categorical Analysis**: Unique values, frequency charts
- 🔗 **Correlations**: Heatmaps showing variable relationships
- ⚠️ **Warnings**: Data quality alerts and recommendations
- 📈 **Visualizations**: Histograms, bar charts, scatter plots
- 🔍 **Missing Values**: Patterns and heatmaps
- 📋 **Sample Data**: Preview of actual data

## Resources

- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/)
- [GitHub Repository](https://github.com/ydataai/ydata-profiling)
- [Examples Gallery](https://ydata-profiling.ydata.ai/examples/)

## Support

For issues or questions about the profiling tool:
1. Check the generated HTML report for insights
2. Review the JSON report for detailed statistics
3. Consult the ydata-profiling documentation
4. Check test files for usage examples
