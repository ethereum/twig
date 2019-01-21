from pathlib import Path
from typing import Iterable

SOURCES_GLOB = "**/*.vy"


def collect_sources(path: Path, glob: str = SOURCES_GLOB) -> Iterable[Path]:
    if path.is_dir():
        return Path(path).glob(glob)
    else:
        raise FileNotFoundError(f"{path} is not a valid directory.")
