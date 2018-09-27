from pathlib import Path

import pytest

from web3 import Web3

TEST_CONTRACTS_DIR = Path(__file__).parent / "contracts"


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
