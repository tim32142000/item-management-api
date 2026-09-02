import sqlite3

DB_NAME = "experiments.db"


def set_db_name(db_name):
    global DB_NAME
    DB_NAME = db_name

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        frequency REAL NOT NULL CHECK (frequency > 0),
        damping REAL NOT NULL CHECK (damping >= 0),
        amplitude REAL NOT NULL CHECK (amplitude > 0)
    )
    """)

    conn.commit()
    conn.close()


def get_experiments():
    with get_connection() as conn:
        cursor = conn.execute("""
        SELECT *
        FROM experiments
        """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]


def get_experiment(id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM experiments
            WHERE id = ?
        """,
            (id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)


def create_experiment(name, frequency, damping, amplitude):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO experiments
            (name, frequency, damping, amplitude)
            VALUES (?, ?, ?, ?)
        """,
            (name, frequency, damping, amplitude),
        )

        conn.commit()

        return cursor.lastrowid


def delete_experiment(id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM experiments
            WHERE id = ?
            """,
            (id,),
        )

        conn.commit()

        return cursor.rowcount > 0


def update_experiment(id: int, name, frequency, damping, amplitude):
    with get_connection() as conn:

        cursor = conn.execute(
            """
            UPDATE experiments
            SET name = ?,
                frequency = ?,
                damping = ?,
                amplitude = ?
            where id = ?
        """,
            (
                name,
                frequency,
                damping,
                amplitude,
                id,
            ),
        )

        conn.commit()

        return cursor.rowcount > 0
