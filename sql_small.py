import sqlite3

DB_NAME = "experiments.db"

conn = sqlite3.connect(DB_NAME)

cursor = conn.execute("""
    SELECT *
    FROM experiments;
""")

print(list(cursor))


try:
    cursor = conn.execute("""
        UPDATE experiments
        SET amplitude = 86
        WHERE id = 1;
    """)

    cursor = conn.execute("""
        UPDATE experiments
        SET something_wrong = 55
        WHERE id = 2;
    """)

except Exception as e:
    print(e)
    conn.rollback()

cursor = conn.execute("""
    SELECT *
    FROM experiments;
""")

print(list(cursor))

conn.close()
