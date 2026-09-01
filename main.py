from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import (
    init_db,
    get_experiments,
    get_experiment,
    create_experiment,
    delete_experiment,
    update_experiment,
)

init_db()

app = FastAPI()


class Experiment(BaseModel):
    name: str
    frequency: float
    damping: float
    amplitude: float


class ExperimentResponse(BaseModel):
    id: int
    name: str
    frequency: float
    damping: float
    amplitude: float


@app.get("/")
def root():
    return {"message": "Experiment API is running"}


@app.post("/experiments", response_model=ExperimentResponse)
def create_experiment_api(experiment: Experiment):
    new_id = create_experiment(
        experiment.name, experiment.frequency, experiment.damping, experiment.amplitude
    )

    return {"id": new_id, **experiment.model_dump()}


@app.get("/experiments", response_model=list[ExperimentResponse])
def get_experiments_api():
    return get_experiments()



@app.get("/experiments/{id}", response_model=ExperimentResponse)
def get_experiment_api(id: int):
    row = get_experiment(id)

    if row is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return dict(row)


@app.delete("/experiments/{id}")
def delete_experiment_api(id: int):
    is_found = delete_experiment(id)

    if not is_found:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return {"message": "Experiment deleted"}


@app.put("/experiments/{id}", response_model=ExperimentResponse)
def update_experiment_api(id: int, experiment: Experiment):
    is_found = update_experiment(
        id,
        experiment.name,
        experiment.frequency,
        experiment.damping,
        experiment.amplitude,
    )

    if not is_found:
        raise HTTPException(status_code=404, detail="Experiment not found")

    row = get_experiment(id)

    return row
