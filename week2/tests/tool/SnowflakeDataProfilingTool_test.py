"""
Test script for SnowflakeDataProfilingTool

This script demonstrates the usage of the SnowflakeDataProfilingTool
for profiling Snowflake data using ydata-profiling.
"""

import sys
import os
from pathlib import Path

from agent.tool.SnowflakeDataProfilingTool import SnowflakeDataProfilingTool


def test_basic_profiling():
    """Test basic data profiling functionality."""
    print("=" * 80)
    print("Testing SnowflakeDataProfilingTool - Basic Profiling")
    print("=" * 80)
    
    # TODO: Create tool instance with reports directory
    # Hint: Use SnowflakeDataProfilingTool(reports_dir="ge_reports")
    
    # TODO: Test connection first
    # Hint: Use tool.test_connection() and check if result['success'] is True
    
    # TODO: Profile a sample query
    # Hint: Use query = "SELECT * FROM RIDEBOOKING LIMIT 500"
    # Call tool.profile_data() with appropriate parameters:
    #   - query: the SQL query
    #   - table_name: a descriptive name for the profiling results
    #   - goal: describe what you're trying to analyze
    #   - generate_html: True to create HTML report
    #   - generate_json: True to create JSON report
    
    # TODO: Check if profiling was successful and print results
    # Hint: Check result['success'] and display:
    #   - Row count
    #   - Column count
    #   - Column names
    #   - Report paths
    #   - Summary metrics (if available)
    
    pass  # Remove this when implementing


def test_custom_query_profiling():
    """Test profiling with a custom aggregated query."""
    print("\n" + "=" * 80)
    print("Testing Custom Query Profiling")
    print("=" * 80)
    
    # TODO: Create tool instance
    
    # TODO: Create an aggregated query to analyze daily statistics
    # Hint: Use SQL aggregation functions like COUNT(), AVG(), SUM()
    # Example columns in RIDEBOOKING table:
    #   - DATE: booking date
    #   - BOOKING_VALUE: transaction amount
    #   - RIDE_DISTANCE: distance traveled
    #   - CUSTOMER_ID: customer identifier
    # Note: Use TRY_CAST() to handle 'null' string values safely
    
    # TODO: Profile the aggregated query
    # Hint: Call tool.profile_data() with your custom query
    
    # TODO: Display profiling results
    
    pass  # Remove this when implementing


def main():
    """Run all tests."""
    try:
        # Test basic profiling
        test_basic_profiling()
        
        # Test custom query profiling
        # test_custom_query_profiling()
        
        print("\n" + "=" * 80)
        print("All tests completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
