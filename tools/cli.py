from __future__ import annotations
import os
import shlex
import subprocess
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv

app = typer.Typer(help="CLI helpers for my-pet-chatbot")

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def run(cmd: str, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and stream output; raise on non-zero if check True."""
    print(f"$ {cmd}")
    p = subprocess.run(cmd, shell=True, cwd=str(cwd or ROOT), text=True)
    if check and p.returncode != 0:
        raise typer.Exit(code=p.returncode)
    return p


@app.command()
def sync():
    """Run dependency sync (uv sync)."""
    run("uv sync")


@app.command()
def activate_env():
    typer.echo("Run this in your shell to activate the venv:")
    typer.echo("source .venv/bin/activate")


@app.command()
def start_mcp(detach: bool = typer.Option(False, "-d", help="Run in background")):
    """Start the MCP service (mcp dev mcp_service.py)."""
    cmd = "mcp dev mcp_service.py"
    if detach:
        cmd = cmd + " &"
    run(cmd)


@app.command()
def start_db(detach: bool = typer.Option(False, "-d", help="Run docker-compose up detached")):
    """Start vector DB via docker-compose (expects docker-compose.yml)."""
    cmd = "docker-compose up"
    if detach:
        cmd = "docker-compose up -d"
    run(cmd)


@app.command()
def run_project():
    """Run the main project entry: uv run python run.py"""
    run("uv run python run.py")


@app.command()
def check_qdrant():
    """Quick health check for Qdrant on localhost:6333"""
    try:
        run("curl -sS http://localhost:6333/health | jq .")
    except Exception:
        typer.echo("Failed to query Qdrant health. Is it running on localhost:6333?")
        raise


@app.command()
def init_env():
    """Load .env and print helpful hints (no shell modification)."""
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH)
        typer.echo(f"Loaded .env from {ENV_PATH}")
    else:
        typer.echo("No .env file found. Create one at project root if needed.")

    typer.echo("Make sure to export ANTHROPIC_API_KEY or GEMINI_API_KEY as needed.")


if __name__ == "__main__":
    app()
