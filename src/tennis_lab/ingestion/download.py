"""Descargas verificadas; una segunda ejecución nunca sobrescribe datos originales."""
from __future__ import annotations

import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


def fingerprints(path: Path) -> dict[str, str | int]:
    payload = path.read_bytes()
    blob = b"blob " + str(len(payload)).encode() + b"\0" + payload
    return {
        "sha256": hashlib.sha256(payload).hexdigest(),
        "git_blob_sha1": hashlib.sha1(blob).hexdigest(),
        "bytes": len(payload),
    }


def verify(path: Path, spec: dict) -> dict:
    actual = fingerprints(path)
    for key in ("sha256", "git_blob_sha1", "bytes"):
        if key in spec and actual[key] != spec[key]:
            raise ValueError(f"Integridad inválida: {path.name}, {key}")
    return actual


def download_source(config_path: Path, destination: Path, workers: int = 4) -> dict:
    config = json.loads(config_path.read_text())
    destination.mkdir(parents=True, exist_ok=True)
    manifest_path = destination / "manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    if previous and previous["revision"] != config["revision"]:
        raise ValueError("Usar otro directorio para una revisión distinta de la fuente")
    locked = {item["name"]: item for item in previous.get("files", [])}

    def obtain(spec: dict) -> dict:
        name = spec["name"]
        if Path(name).name != name:
            raise ValueError(f"Nombre inseguro: {name}")
        path = destination / name
        expected = spec | {k: v for k, v in locked.get(name, {}).items()
                           if k in ("sha256", "git_blob_sha1", "bytes")}
        if not path.exists():
            temporary = path.with_suffix(path.suffix + ".partial")
            try:
                subprocess.run([
                    "curl", "--silent", "--show-error", "--location", "--fail",
                    "--retry", "2", "--max-time", "90", spec["url"],
                    "--output", str(temporary),
                ], check=True)
                verify(temporary, expected)
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
        actual = verify(path, expected)
        return spec | actual

    with ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(obtain, config["files"]))
    manifest = {
        "source": config["source"], "revision": config["revision"],
        "retrieved_at": previous.get("retrieved_at", datetime.now(timezone.utc).isoformat()),
        "files": records,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest
