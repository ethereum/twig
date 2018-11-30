from typing import Any, Dict, Iterable

from eth_utils import to_tuple

from ethpm.tools import builder as b
from vyper import compile_code


@to_tuple
def generate_inline_sources(
    compiler_output: Dict[str, Any]
) -> Iterable[Dict[str, str]]:
    for path in compiler_output.keys():
        contract_type = path.split("/")[-1].split(".")[0]
        yield b.inline_source(contract_type, compiler_output)


@to_tuple
def generate_contract_types(
    compiler_output: Dict[str, Any]
) -> Iterable[Dict[str, Any]]:
    for path in compiler_output.keys():
        contract_type = path.split("/")[-1].split(".")[0]
        yield b.contract_type(contract_type, compiler_output)


def create_raw_asset_data(source: str) -> Dict[str, Any]:
    out = compile_code(source, ["bytecode", "abi"])
    return {
        "abi": out["abi"],
        "evm": {"bytecode": {"object": out["bytecode"], "linkReferences": {}}},
    }
