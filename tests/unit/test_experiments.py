from datetime import date
from pathlib import Path
import pytest
from tennis_lab.experiments import Experiment, load_experiment


def test_season_cutoff_and_cross_year_quarantine():
    experiment = Experiment("stage_1_2025", date(2024, 12, 31), 2025)
    assert experiment.partition(2024, date(2024, 12, 31)) == "train"
    assert experiment.partition(2025, date(2025, 1, 1)) == "evaluation"
    assert experiment.partition(2025, date(2024, 12, 30)) == "quarantine"
    assert experiment.partition(2026, date(2026, 1, 1)) == "future"
    assert experiment.partition(2024, None) == "quarantine"


def test_both_stages_have_disjoint_training_and_evaluation():
    config = Path(__file__).resolve().parents[2] / "configs/experiments.json"
    for name, cutoff, evaluation in (("stage_1_2025", 2024, 2025), ("stage_2_2026", 2025, 2026)):
        experiment = load_experiment(config, name)
        assert experiment.training_cutoff == date(cutoff, 12, 31)
        assert experiment.evaluation_year == evaluation


def test_invalid_experiment_rejected():
    with pytest.raises(ValueError):
        Experiment("leaky", date(2025, 12, 31), 2025)
