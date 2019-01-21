import json
from pathlib import Path

import pytest

from twig import CONTRACTS_DIR
from twig.backends import VyperBackend
from twig.compiler import Compiler
from web3 import Web3

pytest_plugins = ["pytest_ethereum.plugins"]


@pytest.fixture
def w3():
    w3 = Web3(Web3.EthereumTesterProvider())
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3


@pytest.fixture
def test_contracts_dir():
    return Path(__file__).parent / "assets"


@pytest.fixture
def test_contracts_manifest(tmpdir, test_contracts_dir):
    vyper_backend = VyperBackend()
    p = tmpdir.mkdir("test_contracts")
    tmp = p.join("1.0.0.json")
    manifest = Compiler(test_contracts_dir, vyper_backend).get_simple_manifest(
        "twig", "1.0.0"
    )
    tmp.write(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    return Path(p) / "1.0.0.json"


@pytest.fixture
def twig_contracts_manifest(tmpdir):
    vyper_backend = VyperBackend()
    p = tmpdir.mkdir("twig_contracts")
    tmp = p.join("1.0.0.json")
    manifest = Compiler(CONTRACTS_DIR, vyper_backend).get_simple_manifest(
        "twig", "1.0.0"
    )
    tmp.write(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    return Path(p) / "1.0.0.json"


@pytest.fixture
def test_deployer(deployer, test_contracts_manifest):
    return deployer(test_contracts_manifest)


@pytest.fixture
def twig_deployer(deployer, twig_contracts_manifest):
    return deployer(twig_contracts_manifest)
