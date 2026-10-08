"""Construir y auditar las tablas de exploración de la primera etapa."""
import argparse
import json
import sys
import hashlib
import platform
import duckdb
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tennis_lab.experiments import load_experiment
from tennis_lab.ingestion.dataset import build_exploration_dataset
from tennis_lab.ingestion.audit import audit_sources
from tennis_lab.ingestion.report import write_spike_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=["stage_1_2025"], default="stage_1_2025",
                        help="La segunda etapa se habilitará después de revisar la primera")
    args = parser.parse_args()
    experiment = load_experiment(Path("configs/experiments.json"), args.experiment)
    output = Path("data/processed") / experiment.name
    counts = build_exploration_dataset(Path("data/raw"), output, experiment)
    audit = audit_sources(Path("data/raw"), experiment.training_cutoff.year, output,
                          json.loads(Path("configs/official_checks.json").read_text()))
    write_spike_report(audit, counts, Path("docs/data_source_spike.md"))
    code_files = sorted([*Path("src").rglob("*.py"), *Path("scripts").glob("*.py"),
                         *Path("configs").glob("*.json"), Path("pyproject.toml")])
    manifest = {
        "experiment": experiment.name,
        "training_cutoff": experiment.training_cutoff.isoformat(),
        "evaluation_year": experiment.evaluation_year,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "duckdb_version": duckdb.__version__,
        "source_manifests": {
            source: json.loads((Path("data/raw") / source / "manifest.json").read_text())
            for source in ("sackmann", "tml")
        },
        "code_sha256": {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in code_files},
        "partitions": counts,
        "temporal_ready": False,
    }
    (output / "build_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"partitions": counts, "comparison": audit["comparison"]["counts"],
                      "temporal_ready": audit["temporal_ready"]}, indent=2))


if __name__ == "__main__":
    main()
