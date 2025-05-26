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