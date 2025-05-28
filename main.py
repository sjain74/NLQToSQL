import nlqToSqlAgent
from enum import Enum
import utils
import executeQuery
import globals
import argparse
import time

class AgentTypes(Enum):
    NLQ_TO_SQL_OPENAI       = 1
    NLQ_TO_SQL_GOOGLE       = 2
    NLQ_TO_SQL_ANTHROPIC    = 3

VIEW_LOGS = False

# Example use
if __name__ == "__main__":

    agent = AgentTypes.NLQ_TO_SQL_GOOGLE

    parser = argparse.ArgumentParser(description="Natural language query to SQL tool.")
    parser.add_argument("--file", help="Input file containing a list of queries", default=None)
    args = parser.parse_args()

    input_file = open(args.file, "r") if args.file else None
    out_file = open("output.txt", "w")

    utils.load_schema()
    print(f"Schema: {globals.DB_SCHEMA}", file=out_file, flush=True)
    
    while True:
        if input_file:
            time.sleep(10)  # to handle APIs rate limits.
            line = input_file.readline()
            if line:
                query = line.strip()    # skip \n at the end of the line.
                if query[0] == '#':
                    print(f"Skipping: {query}")
                    continue
            else:
                print("Done processing input file!")
                break
        else:
            print("Welcome! Enter a query (or 'exit' to quit):")
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

    if input_file:
        input_file.close()
    out_file.close()