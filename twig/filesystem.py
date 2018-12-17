from pathlib import Path
from typing import Iterable

SOURCES_GLOB = "**/*.vy"


def collect_sources(path: Path, glob: str = SOURCES_GLOB) -> Iterable[Path]:
    return Path(path).glob(glob)
