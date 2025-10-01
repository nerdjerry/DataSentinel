from autogen_agentchat.agents import AssistantAgent
from model.ModelFactory import ModelFactory

class DataQualityAgent:
    def __init__(self, name="DataQualityAgent", description=None):
        self.model = ModelFactory.get_model()
        self.agent = AssistantAgent(
            name=name,
            model_client=self.model,
            description=description or 
            """{
                "role": "You are the DataQualityAgent. Your purpose is to perform data quality analysis on tabular data and produce concise, actionable findings.",
                
                "context": {
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
                "output_format": {
                    "summary": "One-paragraph high-level assessment.",
                    "issues": "List of objects {type, severity (Critical/High/Medium/Low), evidence_query, evidence_description}.",
                    "recommendations": "Ordered remediation steps with estimated priority and impact.",
                    "required_followup_queries": "List of SQL queries to run for deeper investigation (if any)."
                },
                "security_privacy": "Never expose credentials, secrets, or PII in outputs.",
                "insufficient_data_rule": "If data is insufficient to conclude, ask for a specific follow-up query (exact SQL) rather than guessing."
                }
                }"""
        )

    def get_agent(self):
        return self.agent