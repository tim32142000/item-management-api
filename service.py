from database import create_experiment, get_experiment, update_experiment
from database_models import Experiment


def get_experiment_service(id: int) -> Experiment | None:
    return get_experiment(id)


def update_experiment_service(experiment: Experiment) -> Experiment | None:
    if experiment.amplitude > 100:
        raise ValueError("Amplitude can not greater than 100")

    is_found = update_experiment(experiment)

    if not is_found:
        return None

    return experiment


def create_experiment_service(experiment:Experiment) -> Experiment:
    new_id = create_experiment(experiment)
    experiment.id = new_id
    return experiment