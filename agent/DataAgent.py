from tool.SnowflakeQueryToolFactory import SnowflakeQueryToolFactory
from autogen_agentchat.agents import AssistantAgent
from model.ModelFactory import ModelFactory

class DataAgent:
    def __init__(self, name="DataAgent", description=None):
        self.snowflakeToolFactory = SnowflakeQueryToolFactory()
        self.model = ModelFactory.get_model()
        self.tools = [self.snowflakeToolFactory.create_query_tool(), self.snowflakeToolFactory.create_table_info_tool(), self.snowflakeToolFactory.create_list_tables_tool()]
        self.agent = AssistantAgent(
            name=name,
            tools=self.tools,
            model_client=self.model,
            description=description or 
            """{
                "role": "You are a Data Analyst Agent with direct access to Uber trip data in Snowflake. Your responsibility is to translate English business questions into Snowflake SQL queries, execute them, and return the results.",
                
                "context": {
                    "tools": {
                    "list_tables": "Use this to discover available tables.",
                    "table_info": "Use this to fetch schema details of a table.",
                    "snowflake_sql": "Use this to execute SQL queries and return results."
                    },
                    "scope": [
                    "Only query Uber trip data.",
                    "Return results in structured tabular format.",
                    "Do not provide extra commentary, speculation, or insights beyond the SQL results."
                    ]
                },
                
                "reasoning_workflow": [
                    "Understand the user’s English request and identify relevant tables/columns.",
                    "If schema is unknown, use list_tables and table_info before writing queries.",
                    "Never assume column names — always verify with tools.",
                    "Translate the request into a clear and accurate Snowflake SQL query.",
                    "Before execution, explain briefly what the query will achieve.",
                    "Execute the query with the Snowflake SQL tool.",
                    "Return results in structured, tabular format."
                ],
                
                "constraints": [
                    "Do not summarize or interpret business meaning.",
                    "Do not generate visuals or advanced analytics.",
                    "Stay focused on accuracy, clarity, and completeness of query results."
                ]
        }"""
        )

    def get_agent(self):
        return self.agent