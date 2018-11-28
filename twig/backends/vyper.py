from pathlib import Path
from typing import Any, Dict, Iterable, Sequence, Tuple

from eth_utils import to_dict

from twig.utils.compiler import create_raw_asset_data


class VyperBackend:
    def compile(self, sources: Sequence[Path]) -> Dict[str, Any]:
        return generate_vyper_compiler_output(sources)


@to_dict
def generate_vyper_compiler_output(
    all_sources: Sequence[Path]
) -> Iterable[Tuple[str, Any]]:
    for source in all_sources:
        contract_file = str(source).split("/")[-1]
        contract_type = contract_file.split(".")[0]
        # todo fix to accomodate multiple types in a single contract file
        yield str(source), {contract_type: create_raw_asset_data(source.read_text())}
