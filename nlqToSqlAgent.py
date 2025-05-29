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
USE_SEARCH      = None
OPENAI_MODEL    = "gpt-4.1"
GOOGLE_MODEL    = "gemini-2.0-flash"
ANTHROPIC_MODEL = "claude-3-opus-20240229"

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

    prompt = utils.create_prompt(query)

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
    print(f"\n--- Model's Reply ---")
    print(reply)
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

    prompt = utils.create_prompt(query)

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
            return response.text.split('\n', 1)[1].removesuffix("\n```")
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

    import anthropic

def nlq_to_sql_using_anthropic(query: str) -> str:
    """
    AI agent that converts a text string query to SQL query using Anthropic.
    """

    # Configure the API key
    try:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    except KeyError:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it before running the script.")
        exit()

    prompt = utils.create_prompt(query)

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": "You are a helpful SQL assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    reply = response.content[0].text
    print(f"\n--- Model's Reply ---")
    print(reply)
    utils.log_agent_action(query, reply, tool_used="Web Search" if USE_SEARCH else None)
    return reply