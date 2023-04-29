import sqlite3


def initialize_connection():
    """
    Initializes a connection to the SQLite database and returns a connection and cursor object.
    """
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    return conn, cursor


def create_todo_table(cursor):
    """
    Creates a 'tasks' table in the database with the columns id, task, completed, due_date, completion_date, and priority.
    If the table already exists, it will be skipped.
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY,
             task TEXT NOT NULL,
             completed INTEGER,
             due_date DATE,
             completion_date DATE,
             priority INTEGER)''')


def add_demo_tasks(conn, cursor):
    """
    Adds 5 sample tasks to the 'tasks' table in the database.
    """
    cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (?, ?, ?, ?, ?)",
                   ('Finish homework', 0, '2023-05-01', None, 1))
    cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (?, ?, ?, ?, ?)",
                   ('Buy groceries', 0, '2023-05-03', None, 2))
    cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (?, ?, ?, ?, ?)",
                   ('Pay bills', 0, '2023-05-05', None, 3))
    cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (?, ?, ?, ?, ?)",
                   ('Clean house', 0, '2023-05-08', None, 4))
    cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (?, ?, ?, ?, ?)",
                   ('Exercise', 0, '2023-05-10', None, 5))

    # commit the changes and close the connection
    conn.commit()
    close_connection(conn)


def close_connection(conn):
    """
    Closes the connection to the database.
    """
    conn.close()
