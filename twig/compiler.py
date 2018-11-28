from pathlib import Path
from typing import Any, Dict, Sequence

from twig.backends import VyperBackend
from twig.utils.compiler import generate_contract_types, generate_inline_sources


class Compiler:
    def __init__(self, sources: Sequence[Path], backend: VyperBackend) -> None:
        self.sources = sources
        self.backend = backend
        self.output: Dict[str, Any] = None

    def compile(self) -> None:
        self.output = self.backend.compile(self.sources)

    def get_contract_types(self) -> Dict[str, Any]:
        if not self.output:
            self.compile()
        return generate_contract_types(self.output)

    def get_source_tree(self) -> Dict[str, str]:
        if not self.output:
            self.compile()
        return generate_inline_sources(self.output)
