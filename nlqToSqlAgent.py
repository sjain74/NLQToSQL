import openai
import datetime
import requests
from typing import List, Dict

import google.generativeai as genai
import os
from dotenv import load_dotenv
import utils
import globals

LIST_MODELS     = False

"""
SCHEMA   = "Table: customers (id, name, email, city, created_at)\n" + \
           "Table: products (id, name, price, in_stock, created_at)\n" + \
           "Table: orders (id, customer_id, product_id, quantity, order_date, " + \
                "FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (product_id) REFERENCES products(id))"
"""

USE_SEARCH      = None
OPENAI_MODEL    = "gpt-4.1-mini"
GOOGLE_MODEL    = 'gemini-2.0-flash'

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
            You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query.
            Tool info: {tool_info}
            Schema: {globals.DB_SCHEMA}
            Question: {query}
            SQL:
            """
    else:
        return f"""
            You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query.
            Schema: {globals.DB_SCHEMA}
            Question: {query}
            SQL:
            """

def nlq_to_sql_using_openAI(query: str) -> str:
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
    if LIST_MODELS:
        models = openai.models.list()
        for model in models:
            print(model)

    prompt = create_prompt(query)

    print(f"Using model: {OPENAI_MODEL}")
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful SQL assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )

    reply = response.choices[0].message.content
    utils.log_agent_action(query, reply, tool_used="Web Search" if USE_SEARCH else None)
    return reply

def nlq_to_sql_using_google(query: str) -> str:
    """
    AI agent that converts a text string query to SQL query using Google.
    """

    # Configure the API key
    try:
        genai.configure(api_key=os.environ["GOOGLE_AI_API_KEY"])
    except KeyError:
        print("Error: GOOGLE_AI_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        exit()

    # Available models to my API key
    if LIST_MODELS:
        for i, m in zip(range(5), genai.list_models()):
            print(f"Name: {m.name} Description: {m.description} support: {m.supported_generation_methods}")

    prompt = create_prompt(query)

    print(f"Using model: {GOOGLE_MODEL}")
    model = genai.GenerativeModel(GOOGLE_MODEL)
    try:
        # Send the message to the model
        response = model.generate_content(prompt)
        utils.log_agent_action(query, response, tool_used="Web Search" if USE_SEARCH else None)

        # --- Processing the text reply ---
        if response.text:
            print(f"\n--- Model's Text Reply ---")
            print(response.text)
            return response.text.removeprefix("```sql\n").removesuffix("\n```")
        else:
            # This handles cases where the 'text' attribute might be empty
            # but other parts (e.g., content filters) might have information.
            print("\n--- Model's Reply (No direct text found) ---")
            print("Response object:", response)
            print("Candidate count:", len(response.candidates))
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                print(f"Blocked Reason: {response.prompt_feedback.block_reason}")
            elif response.candidates:
                # If there are candidates but no direct .text,
                # you might need to inspect the parts of the first candidate.
                print("Inspecting first candidate's parts:")
                for i, part in enumerate(response.candidates[0].content.parts):
                    print(f"  Part {i}: {part}")
                    if hasattr(part, 'text'):
                        print(f"    Text content: {part.text}")
                        return part.text # Return first text part if found
            return None

    except genai.types.BlockedPromptException as e:
        print(f"\n--- Prompt Blocked ---")
        print(f"Error: {e}")
        print(f"Prompt feedback: {e.response.prompt_feedback}")
        return None
    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(f"Error: {e}")
        return None