from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import typer

app = typer.Typer(invoke_without_command=True)

APP_PATH = str(Path(__file__).parent / "app.py")


@app.callback()
def main() -> None:
    """CLI for the cl-forge Streamlit demo."""


@app.command()
def run(
    uv: bool = typer.Option(False, "--uv", help="Run with 'uv run' instead of 'python -m'"),
) -> None:
    """Launch the Streamlit demo app."""
    if uv:
        cmd = ["uv", "run", "streamlit", "run", APP_PATH]
    else:
        cmd = [sys.executable, "-m", "streamlit", "run", APP_PATH]
    raise SystemExit(subprocess.call(cmd))
