from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from models import ExperimentCreate, ExperimentResponse
from database_models import Experiment

from database import (
    init_db,
    get_experiments,
    delete_experiment,
)

from service import (
    create_experiment_service,
    get_experiments_service,
    get_experiment_service,
    update_experiment_service,
    delete_experiment_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Experiment API is running"}


@app.post(
    "/experiments",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment_api(experiment: ExperimentCreate):
    db_experiment = Experiment(
        name=experiment.name,
        frequency=experiment.frequency,
        damping=experiment.damping,
        amplitude=experiment.amplitude,
    )

    return create_experiment_service(db_experiment)


@app.get("/experiments", response_model=list[ExperimentResponse])
def get_experiments_api():
    return get_experiments_service()


@app.get("/experiments/{id}", response_model=ExperimentResponse)
def get_experiment_api(id: int):
    row = get_experiment_service(id)

    if row is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return row


@app.delete(
    "/experiments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experiment_api(id: int):
    has_found = delete_experiment_service(id)

    if not has_found:
        raise HTTPException(status_code=404, detail="Experiment not found")


@app.put("/experiments/{id}", response_model=ExperimentResponse)
def update_experiment_api(id: int, experiment: ExperimentCreate):
    db_experiment = Experiment(
        id=id,
        name=experiment.name,
        frequency=experiment.frequency,
        damping=experiment.damping,
        amplitude=experiment.amplitude,
    )

    try:
        updated_experiment = update_experiment_service(db_experiment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return updated_experiment
