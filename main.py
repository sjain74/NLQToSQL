import nlqToSqlAgent
from enum import Enum
import utils
import executeQuery
import globals

class AgentTypes(Enum):
    NLQ_TO_SQL_OPENAI       = 1
    NLQ_TO_SQL_GOOGLE       = 2
    NLQ_TO_SQL_ANTHROPIC    = 3

VIEW_LOGS = False

# Example use
if __name__ == "__main__":

    agent = AgentTypes.NLQ_TO_SQL_GOOGLE

    out_file = open("output.txt", "w")

    utils.load_schema()
    print(f"Schema: {globals.DB_SCHEMA}", file=out_file, flush=True)

    print("Welcome! Enter a query (or 'exit' to quit):")
    while True:
        query = input("You: ")
        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        print(f"\nNLQ: {query}", file=out_file, flush=True)

        sql = None
        match agent:
            case AgentTypes.NLQ_TO_SQL_OPENAI:
                sql = nlqToSqlAgent.nlq_to_sql_using_openAI(query)
                
            case AgentTypes.NLQ_TO_SQL_GOOGLE:
                sql = nlqToSqlAgent.nlq_to_sql_using_google(query)

            case AgentTypes.NLQ_TO_SQL_ANTHROPIC:
                sql = nlqToSqlAgent.nlq_to_sql_using_anthropic(query)
                
            case _:
                print("Unknown agent type")

        if VIEW_LOGS:
            print("\n--- Agent Log ---")
            for log in utils.AGENT_LOG:
                print(log)

        if sql:
            print(f"SQL: {sql}", file=out_file, flush=True)
            results = executeQuery.execute_query(sql)

            for row in results:
                print(row)

    out_file.close()