from dataclasses import dataclass


@dataclass
class Experiment:
    name: str
    frequency: float
    damping: float
    amplitude: float
    id: int | None = None
