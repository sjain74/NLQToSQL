import nlqToSqlAgent
from enum import Enum
import utils
import executeQuery

class AgentTypes(Enum):
    NLQ_TO_SQL_OPENAI = 1
    NLQ_TO_SQL_GOOGLE = 2

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

        sql_query = None
        match agent:
            case AgentTypes.NLQ_TO_SQL_OPENAI:
                sql_query = nlqToSqlAgent.nlq_to_sql_using_openAI(query)
                print("Agent Response:\n", sql_query)
                
            case AgentTypes.NLQ_TO_SQL_GOOGLE:
                sql_query = nlqToSqlAgent.nlq_to_sql_using_google(query)
                print(f"Agent Response:\n{sql_query}")
                
            case _:
                print("Unknown agent type")

        if VIEW_LOGS:
            print("\n--- Agent Log ---")
            for log in utils.AGENT_LOG:
                print(log)

        if sql_query:
            results = executeQuery.execute_query(sql_query)

            for row in results:
                print(row)