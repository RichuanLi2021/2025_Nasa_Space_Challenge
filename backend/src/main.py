import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load .env from backend root (parent of src)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from .api import register_routes

API_PREFIX = os.getenv("API_PREFIX", "/api")
app = FastAPI(title="NASA Ice Backend", version="0.1.0")


# CORS: Must be added BEFORE routes
# Enabled wildcard origins because withCredentials is removed from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

@app.get("/health")
def health():
    return {"status": "ok"}


register_routes(app, prefix=API_PREFIX)


def _get_host_port() -> tuple[str, int]:
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port_str = os.getenv("BACKEND_PORT", "5001")
    try:
        port = int(port_str)
    except ValueError as exc:
        raise RuntimeError(f"Invalid BACKEND_PORT '{port_str}' – must be an integer.") from exc
    return host, port


if __name__ == "__main__":
    import uvicorn

    host, port = _get_host_port()
    # When running directly, we assume src is in path or we are inside src.
    # But uvicorn "src.main:app" string requires module path awareness.
    # If we run `python src/main.py`, `uvicorn.run("src.main:app"...)` might fail if `src` is not a package.
    # However, standard usage: cd backend && python -m src.main
    # Or cd backend && uvicorn src.main:app --reload
    uvicorn.run("src.main:app", host=host, port=port, reload=True)
