import sqlite3

from database import (
    create_experiment,
    get_experiment,
    update_experiment,
    delete_experiment,
)
from database_models import Experiment

# Business Rule in this file

DB_NAME = "experiments.db"


def set_db_name(db_name):
    global DB_NAME
    DB_NAME = db_name


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def validate_experiment(experiment: Experiment):
    if experiment.amplitude > 100:
        raise ValueError("Amplitude can not greater than 100")


def get_experiment_service(id: int) -> Experiment | None:
    conn = get_connection()
    return get_experiment(conn, id)


def update_experiment_service(experiment: Experiment) -> Experiment | None:
    conn = get_connection()

    try:
        before_update = get_experiment(conn, experiment.id)

        if before_update is None:
            return None

        validate_experiment(experiment)

        update_experiment(conn, experiment)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return experiment


def create_experiment_service(experiment: Experiment) -> Experiment:
    conn = get_connection()

    try:
        validate_experiment(experiment)

        new_id = create_experiment(conn, experiment)
        experiment.id = new_id

        conn.commit()
    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()

    return experiment


def delete_experiment_service(id: int) -> bool:
    conn = get_connection()

    try:
        before_delete = get_experiment(conn, id)

        if before_delete is None:
            return False

        delete_experiment(conn, id)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return True
