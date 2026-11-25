import subprocess
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


def commit() -> str:
    """The commit this process was started from, so each deploy is visible."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).parent, text=True
        ).strip()
    except Exception:
        return "unknown"


COMMIT = commit()
STARTED_AT = datetime.now(timezone.utc).isoformat()

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (
        "<h1>Hello from VyuhStack</h1>"
        "<p>A FastAPI app deployed on every push.</p>"
        f"<p>Commit <code>{COMMIT}</code>, started <code>{STARTED_AT}</code></p>"
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "commit": COMMIT, "startedAt": STARTED_AT}
