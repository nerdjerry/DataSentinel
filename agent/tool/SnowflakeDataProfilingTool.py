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
        load_dotenv()
        
        # Initialize Snowflake query engine
        self.query_engine = SnowflakeQueryEngine()
        
        # Set up logging
        log_level = os.environ.get('LOG_LEVEL', 'ERROR').upper()
        numeric_level = getattr(logging, log_level, logging.ERROR)
        logging.basicConfig(level=numeric_level)
        self.logger = logging.getLogger(__name__)
        
        # Create reports directory
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"SnowflakeDataProfilingTool initialized. Reports will be saved to: {self.reports_dir}")
    
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
        try:
            self.logger.info(f"Starting data profiling for query: {query}")
            if goal:
                self.logger.info(f"Profiling goal: {goal}")
            
            # Execute query to get data
            query_result = self.query_engine.execute_query(query, goal, "dataframe")
            
            if not query_result['success']:
                return {
                    "success": False,
                    "error": f"Query execution failed: {query_result.get('error', 'Unknown error')}",
                    "query": query
                }
            
            # Get dataframe from query result
            df = query_result['data_frame']
            
            if df.empty:
                return {
                    "success": False,
                    "error": "Query returned no data",
                    "query": query
                }
            
            # Profile data using ydata-profiling
            self.logger.info(f"Profiling {len(df)} rows with {len(df.columns)} columns using ydata-profiling")
            
            # Create profile with ydata-profiling
            profile = ProfileReport(
                df,
                title=f"Data Profile: {table_name}",
                minimal=minimal_mode,
                explorative=not minimal_mode
            )
            
            # Generate reports
            report_paths = {}
            
            if generate_html:
                html_path = self._generate_html_report(profile, table_name, query, goal)
                report_paths['html'] = str(html_path)
            
            if generate_json:
                json_path = self._generate_json_report(profile, table_name, query, goal)
                report_paths['json'] = str(json_path)
            
            # Extract basic summary metrics from the description
            description = profile.get_description()
            table_stats = description.table if hasattr(description, 'table') else {}
            
            return {
                "success": True,
                "query": query,
                "goal": goal,
                "table_name": table_name,
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "summary": {
                    "n_variables": table_stats.get("n_var", len(df.columns)) if isinstance(table_stats, dict) else len(df.columns),
                    "n_observations": table_stats.get("n", len(df)) if isinstance(table_stats, dict) else len(df),
                    "missing_cells": table_stats.get("n_cells_missing", 0) if isinstance(table_stats, dict) else 0,
                    "missing_cells_pct": table_stats.get("p_cells_missing", 0) if isinstance(table_stats, dict) else 0,
                    "duplicate_rows": table_stats.get("n_duplicates", 0) if isinstance(table_stats, dict) else 0,
                    "duplicate_rows_pct": table_stats.get("p_duplicates", 0) if isinstance(table_stats, dict) else 0,
                },
                "report_paths": report_paths,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Data profiling failed: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "query": query,
                "goal": goal,
                "table_name": table_name
            }
    
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
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_filename = f"{table_name}_profile_{timestamp}.html"
            html_path = self.reports_dir / html_filename
            
            # Generate HTML report using ydata-profiling
            profile.to_file(html_path)
            
            self.logger.info(f"HTML report generated: {html_path}")
            return html_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {str(e)}")
            raise
    
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
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_filename = f"{table_name}_profile_{timestamp}.json"
            json_path = self.reports_dir / json_filename
            
            # Use the built-in JSON export from ydata-profiling
            profile.to_file(json_path)
            
            self.logger.info(f"JSON report generated: {json_path}")
            return json_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {str(e)}")
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Snowflake connection.
        
        Returns:
            Dict[str, Any]: Connection test results
        """
        return self.query_engine.test_connection()
