import logging

import pytest

from twig.backends import VyperBackend
from twig.compiler import Compiler

logging.getLogger("evm").setLevel(logging.INFO)


@pytest.fixture
def compiler(test_contracts_dir):
    return Compiler(sources_dir=test_contracts_dir, backend=VyperBackend())


def test_compiler(compiler):
    assert compiler.output is None
    assert len(compiler.get_source_tree()) == 3
    assert len(compiler.get_contract_types()) == 3
    assert isinstance(compiler.backend, VyperBackend)
    assert compiler.output is not None
    auction_data = [
        data["simple_open_auction"]
        for data in compiler.output.values()
        if data.get("simple_open_auction")
    ][0]
    assert "evm" in auction_data
    assert "bytecode" in auction_data["evm"]
    assert "deployedBytecode" in auction_data["evm"]


def test_compiler_creates_valid_registry_package_and_deployment(test_deployer, w3):
    registry_package = test_deployer.deploy("registry")
    registry_contract = registry_package.deployments.get_instance("registry")
    registry_contract.functions.register(b"xxx", w3.eth.accounts[0]).transact()
    actual = registry_contract.functions.lookup(b"xxx").call()
    assert actual == w3.eth.accounts[0]


def test_compiler_creates_valid_auction_package_and_deployment(test_deployer, w3):
    auction_package = test_deployer.deploy(
        "simple_open_auction", w3.eth.accounts[0], 100
    )
    w3 = auction_package.w3
    auction_contract = auction_package.deployments.get_instance("simple_open_auction")
    auction_start = auction_contract.functions.auctionStart().call()
    auction_end = auction_contract.functions.auctionEnd().call()
    assert auction_end - auction_start == 100
