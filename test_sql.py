import sqlite3


conn = sqlite3.connect("experiments.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    frequency REAL NOT NULL,
    damping REAL NOT NULL,
    amplitude REAL NOT NULL
)
""")

conn.execute("""
INSERT INTO experiments
(name, frequency, damping, amplitude)
VALUES (?, ?, ?, ?)
""", ("test", 2.5, 0.2, 4.7))

conn.commit()

cursor = conn.execute("""
SELECT *
FROM experiments
""")

for row in cursor:
    print(row)

cursor2 = conn.execute("""
SELECT *
FROM experiments
WHERE id = ?
""", (id,))
for row in cursor2:
    print(row)

conn.close