from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from eth_utils import to_dict, to_tuple

from ethpm.tools import builder as b
from vyper import compile_code


@to_tuple
def generate_inline_sources(
    compiler_output: Dict[str, Any], sources_dir: Path
) -> Iterable[Dict[str, str]]:
    for path in compiler_output.keys():
        contract_type = path.split("/")[-1].split(".")[0]
        yield b.inline_source(
            contract_type, compiler_output, package_root_dir=sources_dir
        )


@to_tuple
def generate_contract_types(
    compiler_output: Dict[str, Any]
) -> Iterable[Dict[str, Any]]:
    for path in compiler_output.keys():
        contract_type = path.split("/")[-1].split(".")[0]
        yield b.contract_type(contract_type, compiler_output)


@to_dict
def create_raw_asset_data(source: str) -> Iterable[Tuple[str, Any]]:
    out = compile_code(source, ["abi", "bytecode", "bytecode_runtime"])
    yield "abi", out["abi"]
    yield "evm", create_raw_bytecode_object(out)


@to_dict
def create_raw_bytecode_object(
    compiler_output: Dict[str, Any]
) -> Iterable[Tuple[str, Dict[str, Any]]]:
    yield "bytecode", {"object": compiler_output["bytecode"]}
    yield "deployedBytecode", {"object": compiler_output["bytecode_runtime"]}
