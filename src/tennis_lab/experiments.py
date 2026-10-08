"""Separación explícita entre entrenamiento y evaluación por temporada."""
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path


@dataclass(frozen=True)
class Experiment:
    name: str
    training_cutoff: date
    evaluation_year: int

    def __post_init__(self) -> None:
        if self.training_cutoff != date(self.evaluation_year - 1, 12, 31):
            raise ValueError("El corte debe ser el cierre del año previo a la evaluación")

    def partition(self, season: int, tournament_start: date | None) -> str:
        if tournament_start is None or tournament_start.year != season:
            return "quarantine"
        if season < self.evaluation_year and tournament_start <= self.training_cutoff:
            return "train"
        if season == self.evaluation_year:
            return "evaluation"
        return "future"


def load_experiment(path: Path, name: str) -> Experiment:
    config = json.loads(path.read_text())[name]
    return Experiment(name, date.fromisoformat(config["training_cutoff"]),
                      config["evaluation_year"])
