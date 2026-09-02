import sqlite3

DB_NAME = "experiments.db"

with sqlite3.connect(DB_NAME) as conn:

    cursor = conn.execute(
        """
        INSERT INTO experiments
        (name, frequency, damping, amplitude)
        VALUES (?, ?, ?, ?)
    """, ('test', -1, 0.2, 4.7))

    conn.commit()