import sys
from pathlib import Path
from agent.tool.ProfilingReportReaderTool import ProfilingReportReaderTool

if __name__ == "__main__":
    """
    Example usage of the ProfilingReportReaderTool
    """
    try:
        # Create tool instance
        tool = ProfilingReportReaderTool(reports_dir="ge_reports")

        # Check for available reports in the directory
        print("Looking for profiling reports in ge_reports/...")
        reports_dir = Path("ge_reports")
        
        if reports_dir.exists():
            json_files = list(reports_dir.glob("*.json"))
            
            if json_files:
                print(f"Found {len(json_files)} JSON report(s)")
                
                # Read the first report
                report_name = json_files[0].name
                print(f"\nReading report: {report_name}")
                
                read_result = tool.read_json_report(report_name, pretty_print=False)
                
                if read_result["success"]:
                    print(f"Successfully read report!")
                    print(f"File path: {read_result['file_path']}")
                    print(f"Size: {read_result['size_bytes']} bytes")
                    print(f"\nContent preview (first 500 characters):")
                    print(read_result["content"][:500] + "...")
                else:
                    print(f"Error reading report: {read_result['error']}")
            else:
                print("No JSON reports found in the ge_reports directory.")
        else:
            print("The ge_reports directory does not exist.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("- The ge_reports directory exists")
        print("- You have profiling reports generated (*.json files)")
        print("\nYou can generate reports using:")
        print("  python snowflake_example.py")
        print("Or use SnowflakeDataProfilingTool to create profiling reports.")
