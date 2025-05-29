from typing import List, Dict
import datetime
import sqlite3
import globals

# Optional tool: Web search via DuckDuckGo Instant Answer API (simplified example)
def web_search(query: str) -> str:
    response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
    if response.ok:
        data = response.json()
        return data.get("Abstract", "No answer found.")
    return "Search failed."

# Memory/log for agent activity
AGENT_LOG: List[Dict] = []

def log_agent_action(task: str, response: str, tool_used: str = None):
    AGENT_LOG.append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "task": task,
        "response": response,
        "tool": tool_used
    })

def load_schema():
    conn = sqlite3.connect(globals.SQLITE3_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    for sql in cursor.fetchall():
        globals.DB_SCHEMA += sql[0] + "\n"

    print(f"Schema:\n{globals.DB_SCHEMA}")
    conn.close()

def get_info_using_external_tools(query: str) -> str:
    # Decide whether to use a tool based on keywords
    USE_SEARCH = any(keyword in query.lower() for keyword in ["latest", "trends", "examples", "benchmarks"])

    tool_info = None
    if USE_SEARCH:
        search_result = utils.web_search(task)
        tool_info = f"Here is some information from a quick web search:\n{search_result}\n\n"

    return tool_info

def create_prompt(query: str) -> str:
    tool_info = get_info_using_external_tools(query)

    if tool_info:
        return f"""
            You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query for a sqlite3 DB.
            Tool info: {tool_info}
            Schema: {globals.DB_SCHEMA}
            Question: {query}
            SQL:
            """
    else:
        return f"""
            You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query for a sqlite3 DB.
            Schema: {globals.DB_SCHEMA}
            Question: {query}
            SQL:
            """
