from typing import Any, Dict, Iterable

from eth_utils import to_hex, to_tuple

from ethpm.tools import builder as b
from vyper import compiler


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
    return {
        "abi": compiler.mk_full_signature(source),
        "evm": {
            "bytecode": {
                "object": to_hex(compiler.compile(source)),
                "linkReferences": {},
            }
        },
    }
