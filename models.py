from pydantic import BaseModel, Field

class ExperimentCreate(BaseModel):
    name: str
    frequency: float = Field(gt=0)
    damping: float = Field(ge=0)
    amplitude: float = Field(gt=0)


class ExperimentResponse(BaseModel):
    id: int
    name: str
    frequency: float
    damping: float
    amplitude: float