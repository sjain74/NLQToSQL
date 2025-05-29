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
$ python main.py -h
usage: main.py [-h] [-ifile IFILE] [-ofile OFILE]

Natural language query to SQL tool.

options:
  -h, --help    show this help message and exit
  -ifile IFILE  Input file containing a list of natural language queries
  -ofile OFILE  Output file containing the list of the corresponding SQL queries
``` 

## TBDs:

1. With Google AI, and the current shop.db schema:
	1. Try a variety of queries, with column selection, sorting, grouping etc. - DONE, have a test suite of ~60 queries
	2. Check their correctness - DONE, 95%+ queries -> SQL mapping seem to capture the right user intention
	3. Create a test suite - DONE, have a test suite of ~60 queries
	4. See how much is the accuracy - DONE, 95%+ queries -> SQL mapping seem to capture the right user intention
	5. See how accuracy can be improved through prompt improvemts through interactive feedback/clarifiying comments, post-training, RL etc. - Probably not needed right now since the accuracy is pretty good.
2. Perform the above step now with a more complex schema:
	1. Overall, note the limitations of the system
3. Apply techniques from https://cloud.google.com/blog/products/databases/techniques-for-improving-text-to-sql
	1. Problem #1: Provide business-specific context. For example, even the best DBA in the world would not be able to write an accurate query to track shoe sales if they didn't know that cat_id2 = 'Footwear' in a pcat_extension table means that the product in question is a kind of shoe. The same is true for  LLMs.
	2. Problem #2: Understanding user intent. Being able to reply with follow-up questions to disambiguate, explaining the reasoning that went into an answer, and guiding the user to what they are looking for is key.
	3. Problem #3: Limits of LLM generation. As a simple example, if you're using BigQuery SQL, the correct function for extracting a month from a timestamp column is EXTRACT(MONTH FROM timestamp_column). But if you are using MySQL, you use MONTH(timestamp_column).
4. Perform above steps with models from OpenAI and Anthropic - Looks like OpenAI and Anthropic don't offer APIs access in free tier, will postpone this TBD till we have a customer interest.
	1. Test these models with the test suite
	2. Compare which models are performing better
7. Think about some other schemes to improve accuracy e.g. by comparing outputs from different models etc.
8. Add a frontend
9. Dockerize the whole "product"
10. Integrate with Birder.media
11. Dig deeper into other similar works, e.g.: https://levelup.gitconnected.com/how-to-build-a-natural-language-data-querying-agent-with-a-production-ready-co-pilot-24009b86e696
12. Look into the relevance of MCP based architectures in this problem context.
