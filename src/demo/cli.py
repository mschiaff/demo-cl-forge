from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
from contextlib import suppress
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

console = Console()
app = typer.Typer(invoke_without_command=True)

APP_PATH = str(Path(__file__).parent / "app.py")
PID_FILE = Path(tempfile.gettempdir()) / "demo-cl-forge.pid"


def _read_pid() -> int | None:
    """Read PID from file and verify process is alive."""
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)  # signal 0 = alive check, no actual signal sent
        return pid
    except (ValueError, ProcessLookupError, PermissionError):
        PID_FILE.unlink(missing_ok=True)
        return None


def _build_cmd(uv: bool) -> list[str]:
    if uv:
        return ["uv", "run", "streamlit", "run", APP_PATH]
    return [sys.executable, "-m", "streamlit", "run", APP_PATH]


@app.callback()
def main() -> None:
    """CLI for the cl-forge Streamlit demo."""


@app.command()
def run(
    uv: bool = typer.Option(False, "--uv", help="Run with 'uv run' instead of 'python -m'"),
    detach: bool = typer.Option(False, "--detach", help="Run in the background (detached mode)"),
) -> None:
    """Launch the Streamlit demo app."""
    if _read_pid() is not None:
        console.print("[yellow]The app is already running.[/yellow]")
        raise SystemExit(1)

    cmd = _build_cmd(uv)

    if detach:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        PID_FILE.write_text(str(proc.pid))
        console.print(
            Panel.fit(
                f"[green]Streamlit app started in detached mode (PID {proc.pid}).[/green]\n\n"
                "  Local URL:   [link=http://localhost:8501]http://localhost:8501[/link]\n\n"
                "To stop the app, run: [bold]demo stop[/bold]",
            )
        )
    else:
        console.print(
            Panel.fit(
                "[green]Starting Streamlit app...[/green]\n\n"
                "Press [bold]Ctrl+C[/bold] to stop.",
            )
        )
        raise SystemExit(subprocess.call(cmd))


@app.command()
def stop() -> None:
    """Stop a detached Streamlit demo app."""
    pid = _read_pid()
    if pid is None:
        console.print("[yellow]The app is not running.[/yellow]")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        # Wait briefly for graceful shutdown, then force-kill if needed
        with suppress(ChildProcessError):
            os.waitpid(pid, os.WNOHANG)
        console.print(f"[green]Stopped the app (PID {pid}).[/green]")
    except ProcessLookupError:
        console.print("[yellow]The app is not running.[/yellow]")
    finally:
        PID_FILE.unlink(missing_ok=True)
