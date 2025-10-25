"""
Factory for creating AutoGen FunctionTools from ProfilingReportReaderTool.

This module provides a factory class that wraps ProfilingReportReaderTool methods
as AutoGen FunctionTools, enabling agents to read and consume JSON profiling reports.
"""

from agent.tool.ProfilingReportReaderTool import ProfilingReportReaderTool
from autogen_core.tools import FunctionTool


class ProfilingReportReaderToolFactory:
    """
    Factory class to create AutoGen FunctionTools for ProfilingReportReaderTool methods.
    
    This factory wraps the ProfilingReportReaderTool methods to make them available
    as tools that can be used by AutoGen agents.
    """
    
    def __init__(self, reports_dir: str = "ge_reports"):
        """
        Initialize the factory with a ProfilingReportReaderTool instance.
        
        Args:
            reports_dir (str): Default directory path for reading reports
        """
        self.reader_instance = ProfilingReportReaderTool(reports_dir=reports_dir)
    
    def create_read_tool(self):
        """
        Create an AutoGen FunctionTool wrapping the ProfilingReportReaderTool.read_json_report method.
        
        This tool allows agents to read JSON profiling reports and receive them as formatted strings.
        
        Returns:
            FunctionTool: AutoGen tool for reading JSON profiling reports
        """
        # TODO: Implement this method
        # 1. Create and return a FunctionTool instance that wraps self.reader_instance.read_json_report
        # 2. Include an appropriate description explaining what the tool does
        # 3. Set strict=True for the FunctionTool
        # 4. Handle ImportError if autogen-core is not installed
        # Hint: The description should explain that this tool reads JSON profiling reports,
        #       accepts file paths, and returns formatted string output
        raise NotImplementedError("Student implementation required")
