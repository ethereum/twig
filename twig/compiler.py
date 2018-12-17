from pathlib import Path
from typing import Any, Dict, Sequence

from ethpm.tools import builder as b
from ethpm.typing import Manifest
from twig.backends import VyperBackend
from twig.exceptions import CompilerError
from twig.utils.compiler import generate_contract_types, generate_inline_sources


class Compiler:
    # todo solidity backend - start from solc output &/or source contracts
    def __init__(self, sources: Sequence[Path], backend: VyperBackend) -> None:
        self.sources = sources
        self.backend = backend
        self.output: Dict[str, Any] = None

    def compile(self) -> None:
        if self.output:
            raise CompilerError(
                "This instance of Compiler already contains compiler output."
            )
        self.output = self.backend.compile(self.sources)

    def get_contract_types(self) -> Dict[str, Any]:
        if not self.output:
            self.compile()
        return generate_contract_types(self.output)

    def get_source_tree(self) -> Dict[str, str]:
        if not self.output:
            self.compile()
        return generate_inline_sources(self.output)

    def get_simple_manifest(self, name: str, version: str) -> Manifest:
        composed_contract_types = self.get_contract_types()
        composed_inline_sources = self.get_source_tree()
        manifest = b.build(
            {},
            b.package_name(name),
            b.version(version),
            b.manifest_version("2"),
            *composed_inline_sources,
            *composed_contract_types,
            b.validate(),
        )
        return manifest
