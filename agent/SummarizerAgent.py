from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
import json
import os

from agent.tool.ProfilingReportReaderToolFactory import ProfilingReportReaderToolFactory

class DataQualityIssue(BaseModel):
    type: str  # e.g., "Missing Values", "Type Mismatch"
    severity: str  # One of "Critical", "High", "Medium", "Low"
    evidence_query: str  # The SQL query used to gather evidence
    evidence_description: str  # Description of the evidence found
class DataQualityAgentReport(BaseModel):
    summary: str  # One-paragraph high-level assessment
    issues: list[DataQualityIssue]  # List of data quality issues
    recommendations: list[str]  # Ordered remediation steps with estimated priority and impact
    required_followup_queries: list[str]  # List of SQL queries to run for deeper investigation (if any)
    analysis_complete: bool  # Flag to indicate if analysis is complete

class SummarizerAgent:
    def __init__(self, name="SummarizerAgent", system_message=None):
        self.model = ModelFactory.get_model()
        self.profile_reader_factory = ProfilingReportReaderToolFactory(reports_dir="ge_reports")
        self.schema = self._get_schema()
        self.tools = [self.profile_reader_factory.create_read_tool()]
        self.agent = AssistantAgent(
            name=name,
            model_client=self.model,
            description="Summarizer Agent for Data Quality Issue Reporting",
            tools=self.tools,
            system_message=system_message or 
            f"""{json.dumps({
            "role": "You are the SummarizerAgent. Combine outputs from DataAgent and ProfilingAgent to produce a unified data quality summary highlighting key issues, evidence, and recommendations.",

            "schema": self.schema,

            "capabilities": {
                "data_sources": ["DataAgent", "ProfilingAgent"],
                "actions": [
                "Correlate data samples with profiling statistics",
                "Identify discrepancies, anomalies, and type mismatches",
                "Summarize key findings with evidence and remediation steps"
                ]
            },

            "output_format": {
                "summary": "One-paragraph overview of combined findings",
                "issues": [
                {
                    "type": "Missing Values",
                    "severity": "High",
                    "evidence_query": "SELECT COUNT(*) FROM RIDEBOOKING WHERE BOOKING_VALUE IS NULL",
                    "evidence_description": "15% of records have null BOOKING_VALUE"
                }
                ],
                "recommendations": [
                "Impute missing BOOKING_VALUE based on median values"
                ],
                "required_followup_queries": [
                "SELECT BOOKING_VALUE, RIDE_DISTANCE FROM RIDEBOOKING WHERE BOOKING_VALUE IS NULL"
                ],
                "analysis_complete": True
            },

            "constraints": [
                "Correlate DataAgent and ProfilingAgent findings consistently",
                "Use profiling metrics to validate data observations",
                "Never expose credentials, secrets, or PII",
                "Output must match DataQualityAgentReport schema in valid JSON"
            ],

            "termination_condition": "Summarize findings once, produce a complete DataQualityAgentReport, and terminate execution."
            })}""",
            reflect_on_tool_use=False,  # Disabled to prevent JSON parsing issues with structured output
            model_client_stream=False,  # Disable streaming for structured output
            output_content_type=DataQualityAgentReport
        )

    def _get_schema(self):
        """Load table schema from metadata/schema.json"""
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata', 'schema.json')
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Schema file not found at {schema_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in schema file {schema_path}")
            return {}
        
    def get_agent(self):
        return self.agent