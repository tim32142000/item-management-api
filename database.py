import sqlite3

from database_models import Experiment

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


def get_experiments() -> list[Experiment]:
    with get_connection() as conn:
        cursor = conn.execute("""
        SELECT *
        FROM experiments
        """)

        rows = cursor.fetchall()

        return [
            Experiment(
                id=row["id"],
                name=row["name"],
                frequency=row["frequency"],
                damping=row["damping"],
                amplitude=row["amplitude"],
            )
            for row in rows
        ]


def get_experiment(id: int) -> Experiment | None:
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

        experiment = Experiment(
            id=row["id"],
            name=row["name"],
            frequency=row["frequency"],
            damping=row["damping"],
            amplitude=row["amplitude"],
        )


        return experiment


def create_experiment(experiment: Experiment) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO experiments
            (name, frequency, damping, amplitude)
            VALUES (?, ?, ?, ?)
        """,
            (
                experiment.name,
                experiment.frequency,
                experiment.damping,
                experiment.amplitude,
            ),
        )

        conn.commit()

        return cursor.lastrowid


def delete_experiment(id: int) -> bool:
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


def update_experiment(experiment: Experiment) -> bool:
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
                experiment.name,
                experiment.frequency,
                experiment.damping,
                experiment.amplitude,
                experiment.id,
            ),
        )

        conn.commit()

        return cursor.rowcount > 0
