import origSampleAgent 
import nlqToSqlAgent
from enum import Enum
import utils

class AgentTypes(Enum):
    ORIG_SAMPLE_AGENT = 1
    NLQ_TO_SQL_OPENAI = 2
    NLQ_TO_SQL_GOOGLE = 3

# Example use
if __name__ == "__main__":

    agent = AgentTypes.NLQ_TO_SQL_GOOGLE
    match agent:
        case AgentTypes.ORIG_SAMPLE_AGENT:
            task = "What are the latest trends in B2B content marketing in 2025?"
            result = origSampleAgent.smart_marketing_agent(task)
            print("Agent Response:\n", result)
            
        case AgentTypes.NLQ_TO_SQL_OPENAI:
            query = "How many customers do we have?"
            result = nlqToSqlAgent.nlq_to_sql_using_openAI(query)
            print("Agent Response:\n", result)
            
        case AgentTypes.NLQ_TO_SQL_GOOGLE:
            query = "How many customers do we have?"
            result = nlqToSqlAgent.nlq_to_sql_using_google(query)
            print("Agent Response:\n", result)
            
        case _:
            print("Unknown agent type")

    # View log
    print("\n--- Agent Log ---")
    for log in utils.AGENT_LOG:
        print(log)