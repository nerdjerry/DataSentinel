from agent.tool.SnowflakeDataProfilingTool import SnowflakeDataProfilingTool
from autogen_core.tools import FunctionTool

class SnowflakeDataProfilingToolFactory:
    """
    Factory class to create AutoGen FunctionTools for SnowflakeDataProfilingTool methods.
    """
    def __init__(self, reports_dir: str = "ge_reports"):
        """
        Initialize the factory with a SnowflakeDataProfilingTool instance.
        
        Args:
            reports_dir (str): Directory path for storing generated reports
        """
        self.profiling_instance = SnowflakeDataProfilingTool(reports_dir=reports_dir)

    def create_profile_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeDataProfilingTool.profile_data method.

        Returns:
            FunctionTool: AutoGen tool for profiling data with ydata-profiling
        """
        try:
            return FunctionTool(
                self.profiling_instance.profile_data,
                description="""Profile a Snowflake dataset using ydata-profiling. 
                Executes a SQL query, analyzes the data quality, and generates comprehensive 
                interactive HTML and JSON reports with statistics, correlations, missing values analysis, 
                and visualizations. Returns metrics including null counts, data types, distributions, 
                correlations, and quality scores."""
            )
        except ImportError:
            raise ImportError("autogen-core is required. Install with: pip install autogen-core")

    def create_connection_test_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the SnowflakeDataProfilingTool.test_connection method.

        Returns:
            FunctionTool: AutoGen tool for testing Snowflake connection
        """
        try:
            return FunctionTool(
                self.profiling_instance.test_connection,
                description="""Test the Snowflake database connection. 
                Verifies connectivity and returns connection details including database, 
                schema, and warehouse information."""
            )
        except ImportError:
            raise ImportError("autogen-core is required. Install with: pip install autogen-core")
