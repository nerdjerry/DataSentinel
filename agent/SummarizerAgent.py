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

class SummarizerAgent:
    def __init__(self, name="SummarizerAgent", description=None):
        self.model = ModelFactory.get_model()
        self.schema = self._get_schema()
        self.agent = AssistantAgent(
            name=name,
            model_client=self.model,
            description=description or 
            f"""{{
            "role": "You are the SummarizerAgent. Your purpose is to summarize data quality by combining data samples from DataAgent and profiling statistics from ProfilingAgent to produce comprehensive issue reports.",
            
            "schema": {json.dumps(self.schema, indent=2)},
            
            "context": {{
            "data_sources": {{
                "DataAgent": "Retrieve table samples, raw data, and specific query results",
                "ProfilingAgent": "Obtain statistical profiles, distributions, and metadata analysis"
            }},
            "analysis_workflow": [
                "Request data sample from DataAgent",
                "Request profiling statistics from ProfilingAgent",
                "Cross-reference data samples with statistical profiles",
                "Identify discrepancies between expected and actual patterns",
                "Generate comprehensive issue report"
            ],
            "issue_detection": [
                "Compare null counts from profiling with actual data samples",
                "Validate data type consistency between profile and samples",
                "Check distribution anomalies against statistical baselines",
                "Verify uniqueness constraints using profiling metrics",
                "Detect outliers by comparing samples to statistical ranges",
                "Identify format inconsistencies across both sources",
                "Cross-validate referential integrity issues"
            ],
            "output_format": {{
            "summary": "One-paragraph synthesis of findings from both data and profiling analysis.",
            "issues": "List of objects {{type, severity (Critical/High/Medium/Low), evidence_query, evidence_description}} combining insights from both agents.",
            "recommendations": "Prioritized remediation steps based on combined data and statistical evidence.",
            "required_followup_queries": "List of SQL queries for deeper investigation based on findings.",
            "analysis_complete": "Boolean flag indicating if both data and profiling analysis are complete."
            }},
            "collaboration_rules": [
            "Always correlate DataAgent findings with ProfilingAgent statistics",
            "Use profiling metrics to validate data sample observations",
            "Leverage statistical baselines to identify anomalies in data samples"
            ],
            "security_privacy": "Never expose credentials, secrets, or PII in outputs."
            }}
            }}""",
            reflect_on_tool_use=True,
            model_client_stream=True,
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