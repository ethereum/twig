import logging
from pathlib import Path
import pytest

from twig import CONTRACTS_DIR

logging.getLogger("evm").setLevel(logging.INFO)

@pytest.fixture
def registry(twig_deployer):
    return twig_deployer(CONTRACTS_DIR, "twig", "1.0.0")

def test_registry(registry):
    registry_package, address = registry.deploy("registry")
    w3 = registry_package.w3
    registry_contract = registry_package.get_contract_instance("registry", address)
    registry_contract.functions.register(b'xx', w3.eth.accounts[0]).transact()
    actual = registry_contract.functions.lookup(b'xx').call()

    assert actual == w3.eth.accounts[0]
