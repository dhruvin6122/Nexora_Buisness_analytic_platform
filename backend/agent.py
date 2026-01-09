import os
import logging
from typing import List, Optional
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from langchain_core.tools import BaseTool

# Import db connection - verify this exists in backend/db.py
from backend.db import get_db_connection
from backend.prompts import SYSTEM_PREFIX
from backend.guards import validate_sql

# Setup logging
logger = logging.getLogger(__name__)

class SafeQuerySQLDataBaseTool(QuerySQLDataBaseTool):
    """
    Tool for querying a SQL database with mandatory safety checks.
    """
    def _run(self, query: str, run_manager=None) -> str:
        """Execute the query, return the results or an error message."""
        try:
            # 1. Validate SQL
            validate_sql(query)
            # 2. Execute if safe
            return super()._run(query, run_manager)
        except Exception as e:
            logger.error(f"SQL Tool Error: {e}")
            return f"Error: {str(e)}"

class SafeSQLDatabaseToolkit(SQLDatabaseToolkit):
    """
    Custom toolkit that provides the SafeQuerySQLDataBaseTool.
    """
    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        tools = super().get_tools()
        safe_tools = []
        for tool in tools:
            if tool.name == "sql_db_query":
                # Replace the standard query tool with our safe version
                safe_tool = SafeQuerySQLDataBaseTool(
                    db=self.db, 
                    description=tool.description
                )
                safe_tools.append(safe_tool)
            else:
                safe_tools.append(tool)
        return safe_tools

def get_agent_executor(chat_history: list = None):
    """
    Constructs and returns the SQL Agent Executor.
    Args:
        chat_history: List of (role, content) tuples or dictionaries.
    """
    try:
        # 1. Setup DB
        db = get_db_connection()
        
        # 2. Setup LLM
        llm = ChatOpenAI(
            model="gpt-4o", 
            temperature=0
        )
        
        # 3. Setup Toolkit with Safety
        toolkit = SafeSQLDatabaseToolkit(db=db, llm=llm)
        
        # 4. Construct System Prompt with History
        today = datetime.now().strftime("%Y-%m-%d")
        date_context = f"\n\n**Current Date**: {today} (Use this for 'today', 'this month', or determining the current year)."
    
        prompt_suffix = date_context
        if chat_history:
            prompt_suffix += "\n\n**Recent Chat History**:\n"
            for role, content in chat_history:
                 # Handle dict or tuple inputs for robustness
                 r = role if isinstance(role, str) else role.get('role', 'user')
                 c = content if isinstance(content, str) else content.get('content', '')
                 prompt_suffix += f"- {str(r).upper()}: {str(c)}\n"
            prompt_suffix += "\nUse the above history to understand context (e.g., 'previous month', 'that product')."
    
        full_prefix = SYSTEM_PREFIX + prompt_suffix
    
        # 5. Create Agent
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="openai-tools",
            prefix=full_prefix
        )
        
        return agent_executor
        
    except NameError as ne:
        logger.critical(f"Configuration Error (NameError): {ne}")
        raise RuntimeError(f"Backend Configuration Error: {ne}")
    except Exception as e:
        logger.critical(f"Failed to initialize agent: {e}")
        # In a real app we might return a dummy agent or re-raise
        raise RuntimeError(f"Failed to initialize AI agent: {e}")
