import origSampleAgent 
import nlqToSqlAgent
from enum import Enum
import utils

class AgentTypes(Enum):
    ORIG_SAMPLE_AGENT = 1
    NLQ_TO_SQL_OPENAI = 2
    NLQ_TO_SQL_GOOGLE = 3

VIEW_LOGS = False

# Example use
if __name__ == "__main__":

    agent = AgentTypes.NLQ_TO_SQL_GOOGLE

    print("Welcome! Enter a query (or 'exit' to quit):")
    while True:
        query = input("You: ")
        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        match agent:
            case AgentTypes.ORIG_SAMPLE_AGENT:
                result = origSampleAgent.smart_marketing_agent(query)
                print("Agent Response:\n", result)
                
            case AgentTypes.NLQ_TO_SQL_OPENAI:
                result = nlqToSqlAgent.nlq_to_sql_using_openAI(query)
                print("Agent Response:\n", result)
                
            case AgentTypes.NLQ_TO_SQL_GOOGLE:
                result = nlqToSqlAgent.nlq_to_sql_using_google(query)
                print("Agent Response:\n", result)
                
            case _:
                print("Unknown agent type")

        if VIEW_LOGS:
            print("\n--- Agent Log ---")
            for log in utils.AGENT_LOG:
                print(log)