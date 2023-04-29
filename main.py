from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

from db import initialize_connection, create_todo_table, add_demo_tasks, close_connection

# Setting up the api key
import environ
env = environ.Env()
environ.Env.read_env()

API_KEY = env('apikey')

# initialize db connection
conn, cursor = initialize_connection()

# Create the table
create_todo_table(cursor)

# Add demo tasks
add_demo_tasks(conn, cursor)

# Close connection to the database
close_connection(conn)

# Setup
open_db = SQLDatabase.from_uri(
    "sqlite:///todo.db",
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
            question = _DEFAULT_TEMPLATE.format(question=prompt)
            print(db_chain.run(question))


get_prompt()
