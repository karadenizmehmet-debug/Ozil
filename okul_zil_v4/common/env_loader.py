import os
from pathlib import Path

def _candidate_env_paths() -> list[Path]:
    here = Path(__file__).resolve()
    return [
        here.parents[2] / ".env",   # project root
        here.parents[1] / ".env",   # package root fallback
        Path.cwd() / ".env",
    ]

def get_env_value(key: str, fallback: str = "") -> str:
    """Read environment variables from OS env first, then .env file."""
    val = os.environ.get(key)
    if val:
        return val.strip()

    for env_path in _candidate_env_paths():
        if env_path.exists():
            try:
                with env_path.open(encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        name, value = line.split("=", 1)
                        if name.strip() == key:
                            return value.strip()
            except OSError as exc:
                print(f".env okuma hatası ({env_path}): {exc}")
    return fallback
