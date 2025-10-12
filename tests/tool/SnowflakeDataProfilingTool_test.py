"""
Test script for SnowflakeDataProfilingTool

This script demonstrates the usage of the SnowflakeDataProfilingTool
for profiling Snowflake data using ydata-profiling.
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent.tool.SnowflakeDataProfilingTool import SnowflakeDataProfilingTool


def test_basic_profiling():
    """Test basic data profiling functionality."""
    print("=" * 80)
    print("Testing SnowflakeDataProfilingTool - Basic Profiling")
    print("=" * 80)
    
    # Create tool instance
    tool = SnowflakeDataProfilingTool(reports_dir="ge_reports")
    
    # Test connection first
    print("\n1. Testing connection...")
    connection_result = tool.test_connection()
    
    if connection_result['success']:
        print("✓ Connection successful")
        print(f"  Database: {connection_result['details']['database']}")
        print(f"  Schema: {connection_result['details']['schema']}")
        print(f"  Warehouse: {connection_result['details']['warehouse']}")
    else:
        print(f"✗ Connection failed: {connection_result['message']}")
        return
    
    # Profile a sample query
    print("\n2. Profiling sample data...")
    query = "SELECT * FROM RIDEBOOKING LIMIT 500"
    
    result = tool.profile_data(
        query=query,
        table_name="ridebooking_sample",
        goal="Profile Uber ride booking data to understand data quality",
        generate_html=True,
        generate_json=True
    )
    
    if result['success']:
        print("✓ Profiling successful!")
        print(f"\nResults:")
        print(f"  Rows: {result['row_count']}")
        print(f"  Columns: {result['column_count']}")
        print(f"  Column Names: {', '.join(result['columns'])}")
        
        print(f"\n  Reports Generated:")
        for report_type, path in result['report_paths'].items():
            print(f"    {report_type.upper()}: {path}")
        
        # Display summary metrics from ydata-profiling
        if 'summary' in result:
            print(f"\n  Data Summary:")
            summary = result['summary']
            print(f"    Variables: {summary.get('n_variables', 'N/A')}")
            print(f"    Observations: {summary.get('n_observations', 'N/A')}")
            print(f"    Missing Cells: {summary.get('missing_cells', 0)} ({summary.get('missing_cells_pct', 0):.2f}%)")
            print(f"    Duplicate Rows: {summary.get('duplicate_rows', 0)} ({summary.get('duplicate_rows_pct', 0):.2f}%)")
        
        print(f"\n  📊 Open the HTML report for comprehensive analysis including:")
        print(f"     - Variable statistics and distributions")
        print(f"     - Correlations and interactions")
        print(f"     - Missing values analysis")
        print(f"     - Duplicate rows detection")
        print(f"     - Sample data preview")
    else:
        print(f"✗ Profiling failed: {result.get('error', 'Unknown error')}")


def test_custom_query_profiling():
    """Test profiling with a custom aggregated query."""
    print("\n" + "=" * 80)
    print("Testing Custom Query Profiling")
    print("=" * 80)
    
    tool = SnowflakeDataProfilingTool(reports_dir="ge_reports")
    
    # Profile an aggregated query using actual column names from RIDEBOOKING table
    # Columns: DATE, BOOKING_VALUE, RIDE_DISTANCE, etc.
    # Using TRY_CAST to handle 'null' string values safely
    query = """
    SELECT 
        DATE as booking_date,
        COUNT(*) as total_bookings,
        AVG(TRY_CAST(BOOKING_VALUE AS DECIMAL(10,2))) as avg_booking_value,
        SUM(TRY_CAST(BOOKING_VALUE AS DECIMAL(10,2))) as total_revenue,
        AVG(TRY_CAST(RIDE_DISTANCE AS DECIMAL(10,2))) as avg_distance,
        COUNT(DISTINCT CUSTOMER_ID) as unique_customers,
        COUNT(CASE WHEN BOOKING_VALUE IS NULL OR BOOKING_VALUE = 'null' THEN 1 END) as null_booking_values,
        COUNT(CASE WHEN RIDE_DISTANCE IS NULL OR RIDE_DISTANCE = 'null' THEN 1 END) as null_distances
    FROM RIDEBOOKING
    WHERE DATE IS NOT NULL
    GROUP BY DATE
    ORDER BY DATE DESC
    LIMIT 30
    """
    
    result = tool.profile_data(
        query=query,
        table_name="ridebooking_daily_stats",
        goal="Analyze daily booking statistics and revenue trends",
        generate_html=True,
        generate_json=True
    )
    
    if result['success']:
        print("✓ Custom query profiling successful!")
        print(f"\n  Analyzed {result['row_count']} days of data")
        print(f"  Reports: {', '.join(result['report_paths'].keys())}")
    else:
        print(f"✗ Profiling failed: {result.get('error', 'Unknown error')}")


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
