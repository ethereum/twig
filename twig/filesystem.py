from pathlib import Path

SOURCES_GLOB = "**/*.vy"


def collect_sources(path, glob=SOURCES_GLOB):
    all_sources = Path(path).glob(glob)
    return all_sources
