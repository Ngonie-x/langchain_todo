from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

# Setting up the api key
import environ
env = environ.Env()
environ.Env.read_env()

API_KEY = env('apikey')

# Setup
open_db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{env('dbpass')}\@localhost/tasks",
)

# setup llm
llm = OpenAI(temperature=0, openai_api_key=API_KEY)

# Create db chain

_DEFAULT_TEMPLATE = """
Given an input question, first create a syntactically correct sqlite3 query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

{question}
"""


db_chain = SQLDatabaseChain(llm=llm, database=open_db, verbose=True)


def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = _DEFAULT_TEMPLATE.format(question=prompt)
                print(db_chain.run(question))
            except Exception as e:
                print(e)


get_prompt()
