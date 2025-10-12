from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
import json
import os

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

class DataQualityAgent:
    def __init__(self, name="DataQualityAgent", description=None):
        self.model = ModelFactory.get_model()
        self.schema = self._get_schema()
        self.agent = AssistantAgent(
            name=name,
            model_client=self.model,
            description=description or 
            f"""{{
            "role": "You are the DataQualityAgent. Your purpose is to perform data quality analysis on tabular data and produce concise, actionable findings.",
            
            "schema": {json.dumps(self.schema, indent=2)},
            
            "context": {{
                "data_access": "Always use the DataAgent to retrieve any table samples, metadata, aggregates, or statistics required. Do not fabricate data or invent results.",
                "data_requests": "When you need data, specify an exact, minimal SQL query for DataAgent to run, and state the exact columns and row limits required.",
                "analysis_tasks": [
                "Detect and explain missing values.",
                "Identify type mismatches.",
                "Spot distribution anomalies.",
                "Check for duplicates.",
                "Verify referential integrity problems.",
                "Detect outliers.",
                "Find inconsistent formats.",
                "Highlight unexpected null patterns."
                ],
            "output_format": {{
                "summary": "One-paragraph high-level assessment.",
                "issues": "List of objects {{type, severity (Critical/High/Medium/Low), evidence_query, evidence_description}}.",
                "recommendations": "Ordered remediation steps with estimated priority and impact.",
                "required_followup_queries": "List of SQL queries to run for deeper investigation (if any).",
                "analysis_complete": "Boolean flag to indicate if analysis is complete."
            }},
            "security_privacy": "Never expose credentials, secrets, or PII in outputs.",
            "insufficient_data_rule": "If data is insufficient to conclude, ask for a specific follow-up query (exact SQL) rather than guessing."
            }}
            }}""",
            reflect_on_tool_use=True,
            model_client_stream=True,
            output_content_type=DataQualityAgentReport
        )

    def _get_schema(self):
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata', 'schema.json')
        with open(schema_path, 'r') as f:
            return json.load(f)
        
    def get_agent(self):
        return self.agent