from database import (
    create_experiment,
    get_experiments,
    get_experiment,
    update_experiment,
    delete_experiment,
    get_connection,
)
from database_models import Experiment

# Business Rule in this file


def validate_experiment(experiment: Experiment):
    if experiment.amplitude > 100:
        raise ValueError("Amplitude can not greater than 100")


def get_experiments_service() -> list[Experiment]:
    print("service: entered")
    with get_connection() as conn:

        experiments = get_experiments(conn)

        return experiments


def get_experiment_service(id: int) -> Experiment | None:
    with get_connection() as conn:
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


def create_two_experiments_service(
    experiment1: Experiment,
    experiment2: Experiment,
):
    conn = get_connection()

    try:
        id1 = create_experiment(conn, experiment1)
        experiment1.id = id1

        id2 = create_experiment(conn, experiment2)
        experiment2.id = id2

        conn.commit()
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return experiment1, experiment2


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
