"""
Snowflake Data Profiling Tool for AutoGen Agents

This module provides a SnowflakeDataProfilingTool class that integrates ydata-profiling
with Snowflake databases to enable automated, comprehensive data profiling and quality reporting.

Features:
- Connects to Snowflake using existing connection parameters
- Creates data batches from SQL queries
- Automatically profiles datasets using ydata-profiling
- Generates comprehensive, interactive HTML reports with visualizations
- Generates detailed JSON reports with statistics
- Provides extensive data quality metrics, correlations, and insights

Environment Variables Required:
- SNOWFLAKE_ACCOUNT: Snowflake account identifier (required)
- SNOWFLAKE_USER: Username for authentication (required)
- SNOWFLAKE_PASSWORD: Password or PAT token for authentication (required)

Optional Parameters:
- SNOWFLAKE_WAREHOUSE: Warehouse name
- SNOWFLAKE_DATABASE: Database name
- SNOWFLAKE_SCHEMA: Schema name
- SNOWFLAKE_ROLE: Role name

"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import pandas as pd
from dotenv import load_dotenv

# Configure matplotlib to use non-interactive backend BEFORE ydata-profiling import
# This prevents "NSWindow should only be instantiated on the main thread" errors on macOS
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

from ydata_profiling import ProfileReport

try:
    from tool.SnowflakeQueryEngine import SnowflakeQueryEngine
except ImportError:
    # Try relative import if absolute doesn't work
    from .SnowflakeQueryEngine import SnowflakeQueryEngine


class SnowflakeDataProfilingTool:
    """
    A tool for profiling Snowflake data using ydata-profiling.
    
    This class handles connecting to Snowflake, executing queries, profiling data,
    and generating comprehensive, interactive HTML and JSON reports with extensive
    data quality metrics, correlations, and visualizations.
    
    Attributes:
        query_engine (SnowflakeQueryEngine): Snowflake query execution engine
        reports_dir (Path): Directory for storing generated reports
    """
    
    def __init__(self, reports_dir: str = "ge_reports"):
        """
        Initialize the SnowflakeDataProfilingTool.
        
        Args:
            reports_dir (str): Directory path for storing generated reports
        """
        # TODO: Student Implementation
        # 1. Load environment variables using load_dotenv()
        # 2. Initialize the Snowflake query engine (self.query_engine)
        # 3. Set up logging:
        #    - Get LOG_LEVEL from environment (default to 'ERROR')
        #    - Configure logging.basicConfig with appropriate level
        #    - Create a logger instance (self.logger)
        # 4. Create reports directory:
        #    - Convert reports_dir to Path object (self.reports_dir)
        #    - Create directory with parents=True and exist_ok=True
        # 5. Log initialization success message
        
        raise NotImplementedError("Students need to implement the __init__ method")
    
    def profile_data(
        self,
        query: str,
        table_name: str,
        goal: str,
        generate_html: bool,
        generate_json: bool,
        minimal_mode: bool
    ) -> Dict[str, Any]:
        """
        Profile a dataset from a Snowflake query using ydata-profiling.
        
        This method executes the provided SQL query, retrieves the data,
        profiles it using ydata-profiling, and generates comprehensive HTML and/or JSON reports
        with extensive statistics, correlations, missing values analysis, and visualizations.
        
        Args:
            query (str): SQL query to execute
            table_name (str): Name to use for the data asset
            goal (str): Description of what the profiling is trying to achieve
            generate_html (bool): Whether to generate HTML report
            generate_json (bool): Whether to generate JSON report
            minimal_mode (bool): If True, generate minimal profile (faster but less detail)
            
        Returns:
            Dict[str, Any]: Profiling results including metrics and report paths
        """
        # TODO: Student Implementation
        # 1. Log the start of profiling:
        #    - Log info message about starting profiling with the query
        #    - If goal is provided, log the profiling goal
        
        # 2. Execute the query using query_engine:
        #    - Call self.query_engine.execute_query(query, goal, "dataframe")
        #    - Check if result['success'] is False, return error dict
        
        # 3. Validate the dataframe:
        #    - Extract df from query_result['data_frame']
        #    - Check if df is empty, return error dict if so
        
        # 4. Create ProfileReport:
        #    - Log profiling info (rows and columns count)
        #    - Create ProfileReport with:
        #      * df as data
        #      * title as f"Data Profile: {table_name}"
        #      * minimal=minimal_mode
        #      * explorative=not minimal_mode
        
        # 5. Generate reports based on flags:
        #    - Initialize empty report_paths dict
        #    - If generate_html is True:
        #      * Call self._generate_html_report()
        #      * Add path to report_paths['html']
        #    - If generate_json is True:
        #      * Call self._generate_json_report()
        #      * Add path to report_paths['json']
        
        # 6. Extract summary metrics:
        #    - Call profile.get_description()
        #    - Extract table stats (check hasattr for 'table')
        #    - Build summary dict with n_variables, n_observations, etc.
        
        # 7. Return success dictionary with:
        #    - success: True
        #    - query, goal, table_name
        #    - row_count, column_count, columns list
        #    - summary statistics
        #    - report_paths
        #    - timestamp (datetime.now().isoformat())
        
        # 8. Handle exceptions:
        #    - Catch any Exception
        #    - Log error
        #    - Return error dictionary
        
        raise NotImplementedError("Students need to implement the profile_data method")
    
    def _generate_html_report(
        self,
        profile: ProfileReport,
        table_name: str,
        query: str,
        goal: str
    ) -> Path:
        """
        Generate HTML report from ydata-profiling ProfileReport.
        
        Args:
            profile (ProfileReport): ydata-profiling ProfileReport object
            table_name (str): Name of the table/dataset
            query (str): SQL query used
            goal (str): Profiling goal
            
        Returns:
            Path: Path to generated HTML report
        """
        # TODO: Student Implementation
        # 1. Generate timestamp string:
        #    - Use datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 2. Create HTML filename:
        #    - Format as f"{table_name}_profile_{timestamp}.html"
        
        # 3. Create full path:
        #    - Combine self.reports_dir with html_filename using Path
        
        # 4. Generate HTML report:
        #    - Call profile.to_file(html_path)
        
        # 5. Log success:
        #    - Log info message with the generated file path
        
        # 6. Return the html_path
        
        # 7. Handle exceptions:
        #    - Catch any Exception
        #    - Log error with self.logger.error()
        #    - Re-raise the exception
        
        raise NotImplementedError("Students need to implement the _generate_html_report method")
    
    def _generate_json_report(
        self,
        profile: ProfileReport,
        table_name: str,
        query: str,
        goal: str
    ) -> Path:
        """
        Generate JSON report from ydata-profiling ProfileReport.
        
        Args:
            profile (ProfileReport): ydata-profiling ProfileReport object
            table_name (str): Name of the table/dataset
            query (str): SQL query used
            goal (str): Profiling goal
            
        Returns:
            Path: Path to generated JSON report
        """
        # TODO: Student Implementation
        # 1. Generate timestamp string:
        #    - Use datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 2. Create JSON filename:
        #    - Format as f"{table_name}_profile_{timestamp}.json"
        
        # 3. Create full path:
        #    - Combine self.reports_dir with json_filename using Path
        
        # 4. Generate JSON report:
        #    - Call profile.to_file(json_path)
        
        # 5. Log success:
        #    - Log info message with the generated file path
        
        # 6. Return the json_path
        
        # 7. Handle exceptions:
        #    - Catch any Exception
        #    - Log error with self.logger.error()
        #    - Re-raise the exception
        
        raise NotImplementedError("Students need to implement the _generate_json_report method")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Snowflake connection.
        
        Returns:
            Dict[str, Any]: Connection test results
        """
        # TODO: Student Implementation
        # 1. Call the query engine's test_connection method:
        #    - Return self.query_engine.test_connection()
        
        raise NotImplementedError("Students need to implement the test_connection method")
