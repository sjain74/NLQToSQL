import openai
import datetime
import requests
from typing import List, Dict

import google.generativeai as genai
import os
from dotenv import load_dotenv
import utils

LIST_MODELS = True

SCHEMA = "Table: customers (id, name, email, city, created_at)\n" + \
         "Table: products (id, name, price, in_stock, created_at)\n" + \
         "Table: orders (id, customer_id, product_id, quantity, order_date, " + \
            "FOREIGN KEY (customer_id) REFERENCES customers(id), FOREIGN KEY (product_id) REFERENCES products(id))"

def nlq_to_sql_using_openAI(query: str) -> str:
    """
    AI agent that converts a text string query to SQL query using OpenAI.
    """
    # Decide whether to use a tool based on keywords
    use_search = any(keyword in query.lower() for keyword in ["latest", "trends", "examples", "benchmarks"])

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

    prompt = f"""
        You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query.
        Schema: {SCHEMA}
        Question: {query}
        SQL:
        """

    using_model = "gpt-4o-mini"
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
    utils.log_agent_action(query, reply, tool_used="Web Search" if use_search else None)
    return reply

def nlq_to_sql_using_google(query: str) -> str:
    """
    AI agent that converts a text string query to SQL query using Google.
    """

    # Decide whether to use a tool based on keywords
    use_search = any(keyword in query.lower() for keyword in ["latest", "trends", "examples", "benchmarks"])

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

    prompt = f"""
        You are a SQL assistant. Given the schema and a natural language question, write a safe SQL query.
        Schema: {SCHEMA}
        Question: {query}
        SQL:
        """

    using_model = 'gemini-2.0-flash'
    print(f"Using model: {using_model}")
    model = genai.GenerativeModel(using_model)
    chat = model.start_chat()
    reply = chat.send_message(prompt)
    utils.log_agent_action(query, reply, tool_used="Web Search" if use_search else None)
    return reply