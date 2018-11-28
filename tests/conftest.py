from pathlib import Path

import pytest

from twig import CONTRACTS_DIR
from web3 import Web3

TEST_CONTRACTS_DIR = Path(__file__).parent / "assets"

pytest_plugins = ["pytest_ethereum.plugins"]


@pytest.fixture
def w3():
    w3 = Web3(Web3.EthereumTesterProvider())
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3


@pytest.fixture
def tmp_contracts(tmpdir):
    contracts = TEST_CONTRACTS_DIR.glob("*.vy")
    p = tmpdir.mkdir("contracts")
    for contract in contracts:
        tmp = p.join(contract.name)
        tmp.write(contract.read_text())
    return p


@pytest.fixture
def deployer(twig_deployer):
    return twig_deployer(CONTRACTS_DIR)
