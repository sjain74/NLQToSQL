import openai
import datetime
import requests
from typing import List, Dict

import google.generativeai as genai
import os
from dotenv import load_dotenv

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

# Original sample agent function with simple tool routing
def smart_marketing_agent(task: str) -> str:
    """
    AI agent that handles a marketing task with optional web search tool support.
    """
    # Decide whether to use a tool based on keywords
    use_search = any(keyword in task.lower() for keyword in ["latest", "trends", "examples", "benchmarks"])
    
    tool_info = ""
    if use_search:
        search_result = web_search(task)
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
    log_agent_action(task, reply, tool_used="Web Search" if use_search else None)
    return reply


SCHEMA = "Table: customers (id, name, email, city, created_at)\n" + \
         "Table: products (id, name, price, in_stock, created_at)\n" + \
         "Table: orders (id, customer_id, product_id, quantity, order_date, " + \
            "FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (product_id) REFERENCES products(id))"

def text_to_sql_using_openAI(query: str) -> str:
    """
    AI agent that converts a text string query to SQL query using OpenAI.
    """

    # Configure the API key
    try:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    except KeyError:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        exit()

    # Available models to my API key
    if False:
        models = openai.models.list()
        for model in models:
            print(model)

    prompt = f"""
        You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query.
        Schema: {SCHEMA}
        Question: {query}
        SQL:
        """

    using_model = "gpt-4o"
    print(f"Using model: {using_model}")
    response = openai.chat.completions.create(
        model=using_model,
        messages=[
            {"role": "system", "content": "You are a helpful SQL assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )

    reply = response.choices[0].message.content
    log_agent_action(query, reply, tool_used="Web Search" if use_search else None)
    return reply

def text_to_sql_using_googleAI(query: str) -> str:

    # Configure the API key
    try:
        genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])
    except KeyError:
        print("Error: GOOGLE_AI_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        exit()

    # Available models to my API key
    if False:
        for i, m in zip(range(5), genai.list_models()):
            print(f"Name: {m.name} Description: {m.description} support: {m.supported_generation_methods}")

    prompt = f"""
        You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query.
        Schema: {SCHEMA}
        Question: {query}
        SQL:
        """

    using_model = 'gemini-1.5-pro-latest'
    print(f"Using model: {using_model}")
    model = genai.GenerativeModel(using_model)
    chat = model.start_chat()
    reply = chat.send_message(prompt)
    log_agent_action(query, reply, tool_used="Web Search" if use_search else None)
    return reply

# Example use
if __name__ == "__main__":

    original = False
    if original:
        task = "What are the latest trends in B2B content marketing in 2025?"
        result = smart_marketing_agent(task)
        print("Agent Response:\n", result)
    else:
        task = "How many customers do we have?"
        result = text_to_sql_using_openAI(task)
        print("Agent Response:\n", result)

    # View log
    print("\n--- Agent Log ---")
    for log in AGENT_LOG:
        print(log)