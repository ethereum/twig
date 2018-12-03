import logging

import pytest

from ethpm.tools import builder as b
from pytest_ethereum.deployer import Deployer
from twig.backends import VyperBackend
from twig.compiler import Compiler
from twig.filesystem import collect_sources

logging.getLogger("evm").setLevel(logging.INFO)


@pytest.fixture
def compiler(tmp_contracts):
    return Compiler(sources=collect_sources(tmp_contracts), backend=VyperBackend())


@pytest.fixture
def twig_deployer(compiler, w3):
    # Return a Deployer containing all .vy contracts found
    sources = compiler.get_source_tree()
    contract_types = compiler.get_contract_types()
    pkg = b.build(
        b.init_manifest("twig", "1.0.0"), *sources, *contract_types, b.as_package(w3)
    )
    return Deployer(pkg)


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


def test_compiler_creates_valid_registry_package_and_deployment(twig_deployer, w3):
    registry_package = twig_deployer.deploy("registry")
    registry_contract = registry_package.deployments.get_instance("registry")
    registry_contract.functions.register(b"xxx", w3.eth.accounts[0]).transact()
    actual = registry_contract.functions.lookup(b"xxx").call()
    assert actual == w3.eth.accounts[0]


def test_compiler_creates_valid_auction_package_and_deployment(twig_deployer, w3):
    auction_package = twig_deployer.deploy(
        "simple_open_auction", w3.eth.accounts[0], 100
    )
    w3 = auction_package.w3
    auction_contract = auction_package.deployments.get_instance("simple_open_auction")
    auction_start = auction_contract.functions.auction_start().call()
    auction_end = auction_contract.functions.auction_end().call()
    assert auction_end - auction_start == 100
