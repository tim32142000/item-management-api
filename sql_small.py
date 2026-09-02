import sqlite3

DB_NAME = "experiments.db"

with sqlite3.connect(DB_NAME) as conn:

    cursor = conn.execute(
        """
        EXPLAIN QUERY PLAN
        SELECT *
        FROM experiments
        WHERE name = 'test experiment';
    """)

    print(list(cursor))