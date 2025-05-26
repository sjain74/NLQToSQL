import openai
import utils

# Original sample agent function with simple tool routing
def smart_marketing_agent(task: str) -> str:
    """
    AI agent that handles a marketing task with optional web search tool support.
    """
    # Decide whether to use a tool based on keywords
    use_search = any(keyword in task.lower() for keyword in ["latest", "trends", "examples", "benchmarks"])
    
    tool_info = ""
    if use_search:
        search_result = utils.web_search(task)
        tool_info = f"Here is some information from a quick search:\n{search_result}\n\n"

    prompt = f"""
    You are a marketing assistant. Help with the following task:

    Task: {task}

    {tool_info}Be concise, professional, and use a helpful tone.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful marketing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )

    reply = response['choices'][0]['message']['content']
    utils.log_agent_action(task, reply, tool_used="Web Search" if use_search else None)
    return reply