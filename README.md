# NLQToSQL
Natural language query to SQL LLM/agent project

## Steps to play around with this agent on mac:

1. Clone the repository
2. In nlqToSql directory:
	1. run "python createSqliteDB.py" to create a sample Sqlite3 DB called shop.db
	2. run "python createSampleData.py" to populate this DB with 1000 customers, 500 products, and 10000 orders
3. You can install "DB browser for Sqlite" to access shop.db
4. Command line:
```
$ python main.py --help
usage: main.py [-h] [--file FILE]
Natural language query to SQL tool.

options:
	-h, --help   show this help message and exit
	--file FILE  Input file containing a list of queries
``` 

## TBDs:

1. With Google AI, and the current shop.db schema:
	1. Try a variety of queries, with column selection, sorting, grouping etc.
	2. Check their correctness
	3. Create a test suite
	4. See how much is the accuracy
	5. See how accuracy can be improved through prompt improvemts through interactive feedback/clarifiying comments, post-training, RL etc.
2. Perform the above step now with a more complex schema:
	1. Overall, note the limitations of the system
	2. Apply techniques from https://cloud.google.com/blog/products/databases/techniques-for-improving-text-to-sql
3. Perform above steps with models from OpenAI and Anthropic
4. Test these models with the test suite
5. Compare which models are performing better
6. Think about some other schemes to improve accuracy e.g. by comparing outputs from different models etc.
7. Add a frontend
8. Dockerize the whole "product"
9. Integrate with Birder.media
10. Dig deeper into other similar works, e.g.: https://levelup.gitconnected.com/how-to-build-a-natural-language-data-querying-agent-with-a-production-ready-co-pilot-24009b86e696