"""Descargar una versión fija de las fuentes; ejecutar desde la raíz del proyecto."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tennis_lab.ingestion.download import download_source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["sackmann", "tml", "mcp", "challenger"], default="sackmann")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    result = download_source(Path(f"configs/{args.source}_source.json"),
                             Path(f"data/raw/{args.source}"), args.workers)
    print(f"{result['source']}: {len(result['files'])} archivos verificados")


if __name__ == "__main__":
    main()
