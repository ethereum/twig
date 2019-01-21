from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from eth_utils import to_dict

from twig.filesystem import collect_sources
from twig.utils.compiler import create_raw_asset_data


class VyperBackend:
    def compile(self, sources_dir: Path) -> Dict[str, Any]:
        return generate_vyper_compiler_output(sources_dir)


@to_dict
def generate_vyper_compiler_output(sources_dir: Path) -> Iterable[Tuple[str, Any]]:
    all_sources = collect_sources(sources_dir)
    for source in all_sources:
        contract_file = str(source).split("/")[-1]
        contract_type = contract_file.split(".")[0]
        # todo fix to accomodate multiple types in a single contract file.
        yield contract_file, {contract_type: create_raw_asset_data(source.read_text())}
